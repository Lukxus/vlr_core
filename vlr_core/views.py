import base64
import io
import urllib

import numpy as np
import seaborn as sns
from django.core.paginator import Paginator
from django.db.models import F, Count, Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from matplotlib import pyplot as plt

from vlr_core.jogador.atributos import ATTRIBUTOS_DE_PARA
from vlr_core.jogador.grafico_service import GraficoService
from vlr_core.jogador.jogadores_service import JogadoresService
from vlr_core.jogador.utils.grafico_radial_service import GraficoRadialService
from vlr_core.models import Time
from vlr_core.partidas.service.partida_service import PartidaService
from vlr_core.times.service.time_service import TimeService


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
        return TimeService.get_times(query)  # Agora usando o TimeService para obter os times com vitórias anotadas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = int(self.request.GET.get('paginate_by', 5))

        times_list = self.get_queryset()
        page = self.request.GET.get('page')

        context.update({
            'page_obj': TimeService.paginate_times(times_list, paginate_by, page),
            'query': self.request.GET.get('q', ''),
            'paginate_by': paginate_by,
            'grafico': self.gerar_histograma(times_list[:10]),  # Gere o gráfico com base nos 10 times com mais vitórias
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

        ultimas_partidas = PartidaService.get_ultimas_partidas(time)
        total_vitorias = PartidaService.get_total_vitorias(time)
        total_partidas = PartidaService.get_total_partidas(time)

        context.update({
            'partidas': ultimas_partidas,
            'total_vitorias': total_vitorias,
            'total_partidas': total_partidas,
        })
        return context


class GraficoRadialView(TemplateView):
    template_name = "grafico_radial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jogador_nome = self.request.GET.get('jogador_nome')
        categoria = self.request.GET.get('categoria', 'geral')

        if jogador_nome:
            context['grafico_radial'] = GraficoRadialService.get_grafico_radial(jogador_nome, categoria)
            context['jogador_nome'] = jogador_nome
            context['categoria'] = categoria

        return context
