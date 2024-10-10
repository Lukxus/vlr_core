from datetime import datetime

from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure
from django.views.generic import TemplateView, ListView

from vlr_core.jogador.JogadorService import JogadorService


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

        if nome and atributo:
            try:
                dados = service.buscar_dados_para_grafico(nome, atributo, nome_time, agente)

                if dados:
                    # Separar datas e valores
                    datas, valores = zip(*dados)
                    source = ColumnDataSource(data={'x': datas, 'y': valores})

                    # Configurar o gráfico
                    p = figure(
                        x_axis_type="datetime",
                        title=f"Evolução do {atributo}",
                        height=350,
                        width=800,
                        tools="pan,wheel_zoom,box_zoom,reset"
                    )

                    # Adicionar linha e pontos com hover
                    p.line('x', 'y', source=source, line_width=2, legend_label=f"{atributo}", color="navy")
                    p.circle('x', 'y', source=source, size=8, color="red", alpha=0.5)

                    # Configurar ferramenta de hover
                    hover = HoverTool(tooltips=[("Data", "@x{%F}"), ("Valor", "@y")], formatters={'@x': 'datetime'})
                    p.add_tools(hover)

                    # Estilização adicional
                    p.title.text_font_size = "16pt"
                    p.xaxis.axis_label = "Data"
                    p.yaxis.axis_label = "Valor"
                    p.legend.location = "top_left"

                    # Renderizar os componentes Bokeh
                    script, div = components(p)
                    context['bokeh_script'] = script
                    context['bokeh_div'] = div
                else:
                    context['error_message'] = "Nenhum dado encontrado para a combinação de filtros aplicada."
            except Exception as e:
                context['error_message'] = f"Ocorreu um erro ao buscar os dados: {str(e)}"
        else:
            context['error_message'] = "Os filtros 'nome' e 'atributo' são obrigatórios."

        return context