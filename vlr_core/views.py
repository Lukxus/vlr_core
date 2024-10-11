from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from utils.ATRIBUTOS import ATTRIBUTOS_DE_PARA
from vlr_core.jogador.JogadorService import JogadorService
from vlr_core.times.TimeService import TimeService


class HomeView(TemplateView):
    template_name = "home.html"

class ListaJogadoresView(TemplateView):
    template_name = 'lista_jogadores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nome = self.request.GET.get('nome')
        nome_time = self.request.GET.get('nome_time')
        page = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('page_size', 10)

        service = JogadorService()
        jogadores = service.listar_jogadores(nome, nome_time, page, page_size)

        context['jogadores'] = jogadores
        context['page_size'] = page_size
        return context

class GraficoAtributoView(TemplateView):
    template_name = 'grafico_atributo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nome = self.request.GET.get('nome')
        atributo = self.request.GET.get('atributo')
        nome_time = self.request.GET.get('nome_time')
        agente = self.request.GET.get('agente')

        service = JogadorService()
        context['agentes'] = service.listar_agentes()

        # Passando os atributos disponíveis do dicionário ATTRIBUTOS_DE_PARA
        context['atributos'] = [(chave, valor) for chave, valor in ATTRIBUTOS_DE_PARA.items()]

        if nome and atributo:
            dados = service.buscar_dados_para_grafico(nome, atributo, nome_time, agente)

            if dados:
                datas, valores = zip(*dados)
                p = figure(x_axis_type="datetime", title=f"Evolução do {atributo}", height=350, width=800)
                p.line(datas, valores, line_width=2)
                script, div = components(p)
                context['bokeh_script'] = script
                context['bokeh_div'] = div
            else:
                context['error_message'] = "Nenhum dado encontrado para a combinação de filtros aplicada."
        else:
            context['error_message'] = "Os filtros 'nome' e 'atributo' são obrigatórios."

        return context

class ListaTimesView(TemplateView):
    template_name = 'lista_times.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nome = self.request.GET.get('nome')
        page = int(self.request.GET.get('page', 1))
        page_size = int(self.request.GET.get('page_size', 10))

        time_service = TimeService()
        context['times'] = time_service.listar_times(nome, page, page_size)

        # Gerar gráfico de barras com os 20 times com mais vitórias
        top_times = time_service.listar_top_times_por_vitorias()
        nomes_times = [time.nome for time in top_times]
        vitorias = [time.vitorias for time in top_times]

        p = figure(x_range=nomes_times, title="Top 20 Times por Vitórias", toolbar_location=None, tools="")
        p.vbar(x=nomes_times, top=vitorias, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = 1.2

        script, div = components(p)
        context['bokeh_script'] = script
        context['bokeh_div'] = div

        return context

class DetalhesTimeView(TemplateView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_service = TimeService()

    def get(self, request, id):
        # Obtendo o número da página da query string, se disponível
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        # Chamando o serviço para obter as partidas e os totais de vitórias e derrotas
        resultado = self.time_service.listar_partidas_por_time(id, page, page_size)
        partidas = resultado['partidas']
        total_vitorias = resultado['total_vitorias']
        total_derrotas = resultado['total_derrotas']

        # Renderizando o template com os dados
        return render(request, 'detalhes_time.html', {
            'partidas': partidas,
            'total_vitorias': total_vitorias,
            'total_derrotas': total_derrotas,
            'time_id': id
        })