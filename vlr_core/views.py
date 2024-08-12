import base64
import io
import urllib

import numpy as np
import seaborn as sns
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from matplotlib import pyplot as plt

from vlr_core.models import Partida, Time
from vlr_core.services.jogador.atributos import ATTRIBUTOS_DE_PARA
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
        sns.barplot(x=nomes, y=vitorias, palette="Blues_d", hue=nomes, legend=False)

        plt.xlabel('Times', fontsize=14)
        plt.ylabel('Número de Vitórias', fontsize=14)
        plt.title('Distribuição de Vitórias dos Top 10 Times', fontsize=16)

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


class GraficoRadialView(TemplateView):
    template_name = "grafico_radial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jogador_nome = self.request.GET.get('jogador_nome')
        categoria = self.request.GET.get('categoria', 'geral')  # 'ataque', 'defesa', 'geral'

        if jogador_nome:
            estatisticas_medias = JogadoresService.get_estatisticas_jogador_por_nome(jogador_nome)
            if estatisticas_medias:
                atributos_filtrados = {key: value for key, value in estatisticas_medias.items() if categoria in key}
                context['grafico_radial'] = self.gerar_grafico_radial(atributos_filtrados)
                context['jogador_nome'] = jogador_nome
                context['categoria'] = categoria

        return context

    def gerar_grafico_radial(self, estatisticas):
        labels = [ATTRIBUTOS_DE_PARA[key] for key in estatisticas.keys()]
        stats = list(estatisticas.values())

        # Normalizar cada estatística de acordo com o seu próprio valor máximo
        stats_normalizados = []
        for key, valor in estatisticas.items():
            max_valor = max(estatisticas.values())  # Substitua esta linha pelo valor máximo esperado para cada atributo específico.
            if max_valor != 0:
                stats_normalizados.append(valor / max_valor)
            else:
                stats_normalizados.append(0)  # Se o máximo é zero, atribui 0 ao valor normalizado

        # Repetir o primeiro valor no final para fechar o gráfico radial
        stats_normalizados += stats_normalizados[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats_normalizados, color='blue', alpha=0.25)
        ax.plot(angles, stats_normalizados, color='blue', linewidth=2)

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        return 'data:image/png;base64,' + urllib.parse.quote(string)
