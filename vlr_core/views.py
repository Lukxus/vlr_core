import base64
import io
import urllib

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from matplotlib import pyplot as plt
import seaborn as sns

from vlr_core.models import Partida, Time
from vlr_core.services.jogador.grafico_service import GraficoService
from vlr_core.services.jogador.jogadores_service import JogadoresService
from vlr_core.services.times.time_service import TimeService


class HomeView(TemplateView):
    template_name = "home.html"


class ListaJogadoresView(ListView):
    template_name = "jogadores.html"
    context_object_name = "page_obj"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        team_query = self.request.GET.get('team', '')
        return JogadoresService.get_jogadores(query, team_query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = int(self.request.GET.get('paginate_by', 5))

        jogadores_list = self.get_queryset()
        paginator = Paginator(jogadores_list, paginate_by)
        page = self.request.GET.get('page')

        context.update({
            'page_obj': paginator.get_page(page),
            'query': self.request.GET.get('q', ''),
            'team_query': self.request.GET.get('team', ''),
            'paginate_by': paginate_by,
        })
        return context


def grafico_atributo(request):
    context = GraficoService().get_grafico_context(request)
    return render(request, 'grafico_atributo.html', context)


class ListaTimesView(ListView):
    template_name = "times.html"
    context_object_name = "page_obj"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return TimeService.get_times(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = int(self.request.GET.get('paginate_by', 5))

        times_list = self.get_queryset()
        page = self.request.GET.get('page')

        context.update({
            'page_obj': TimeService.paginate_times(times_list, paginate_by, page),
            'query': self.request.GET.get('q', ''),
            'paginate_by': paginate_by,
            'grafico': self.gerar_histograma(TimeService.get_top_10_times_com_mais_vitorias()),
        })
        return context

    def gerar_histograma(self, top_10_times):
        vitorias = [time.vitorias for time in top_10_times]
        nomes = [time.nome for time in top_10_times]

        plt.figure(figsize=(12, 6))
        sns.barplot(x=nomes, y=vitorias, palette="Blues_d")
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        string = base64.b64encode(buf.read())
        return 'data:image/png;base64,' + urllib.parse.quote(string)


class TimeDetalhesView(DetailView):
    model = Time
    template_name = "time_detalhes.html"
    context_object_name = "time"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time = self.get_object()

        # Obtém as últimas 5 partidas em que o time participou
        ultimas_partidas = Partida.objects.filter(
            sequencia_partida__time1=time
        ).order_by('-sequencia_partida__data')[:5]

        # Calcula o número total de vitórias
        total_vitorias = Partida.objects.filter(
            sequencia_partida__time1=time, time_vencedor=time
        ).count()

        # Calcula o número total de partidas jogadas pelo time
        total_partidas = Partida.objects.filter(sequencia_partida__time1=time).count()

        context.update({
            'partidas': ultimas_partidas,
            'total_vitorias': total_vitorias,
            'total_partidas': total_partidas,  # Adiciona o número total de partidas ao contexto
        })
        return context
