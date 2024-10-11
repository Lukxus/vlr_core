from bokeh.embed import components
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


class CompararJogadoresView(View):
    template_name = 'comparar_jogadores.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        jogador1_nome = request.POST.get('jogador1', '').strip()
        jogador2_nome = request.POST.get('jogador2', '').strip()
        categoria = request.POST.get('categoria', 'geral')  # Opções: geral, defesa, ataque

        service = JogadorService()

        dados_jogador1 = None
        dados_jogador2 = None

        if not jogador1_nome and not jogador2_nome:
            context = {'error_message': 'Por favor, preencha pelo menos um nome de jogador.'}
            return render(request, self.template_name, context)

        # Obter dados do jogador 1, se fornecido
        if jogador1_nome:
            dados_jogador1 = service.obter_dados_para_comparacao(jogador1_nome, categoria)
            if not dados_jogador1:
                context = {
                    'error_message': f'O jogador "{jogador1_nome}" não foi encontrado ou não possui dados suficientes.'}
                return render(request, self.template_name, context)

        # Obter dados do jogador 2, se fornecido
        if jogador2_nome:
            dados_jogador2 = service.obter_dados_para_comparacao(jogador2_nome, categoria)
            if not dados_jogador2:
                context = {
                    'error_message': f'O jogador "{jogador2_nome}" não foi encontrado ou não possui dados suficientes.'}
                return render(request, self.template_name, context)

        # Gerar o gráfico radial
        script, div = gerar_grafico_radial(
            dados_jogador1, dados_jogador2,
            jogador1_nome if dados_jogador1 else None,
            jogador2_nome if dados_jogador2 else None
        )

        context = {
            'bokeh_script': script,
            'bokeh_div': div,
            'jogador1_nome': jogador1_nome,
            'jogador2_nome': jogador2_nome,
        }
        return render(request, self.template_name, context)


def gerar_grafico_radial(dados_jogador1, dados_jogador2, nome_jogador1, nome_jogador2):
    import math
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource, HoverTool, LabelSet
    from bokeh.embed import components

    atributos = ['ACS', 'KDA', 'ADR', 'HS', 'KAST']

    # Preparar valores e normalizar
    valores_jogadores = []
    max_valor = 0

    if dados_jogador1:
        jogador1_valores = [dados_jogador1.get(attr, 0) or 0 for attr in atributos]
        max_valor = max(max_valor, max(jogador1_valores))
        valores_jogadores.append({
            'nome': nome_jogador1,
            'valores': jogador1_valores,
            'cor': 'blue'
        })

    if dados_jogador2:
        jogador2_valores = [dados_jogador2.get(attr, 0) or 0 for attr in atributos]
        max_valor = max(max_valor, max(jogador2_valores))
        valores_jogadores.append({
            'nome': nome_jogador2,
            'valores': jogador2_valores,
            'cor': 'red'
        })

    if max_valor == 0:
        max_valor = 1  # Evitar divisão por zero

    angulos = [n / float(len(atributos)) * 2 * math.pi for n in range(len(atributos))]
    angulos += angulos[:1]  # Fechar o gráfico

    p = figure(title="Comparação de Atributos", x_range=(-1.2, 1.2), y_range=(-1.2, 1.2),
               toolbar_location=None, tools="")

    p.toolbar.logo = None

    # Desenhar linhas de grade circulares
    num_circulos = 5
    circulos = [i / num_circulos for i in range(1, num_circulos + 1)]
    for r in circulos:
        p.circle(0, 0, radius=r, fill_color=None, line_color='gray', line_dash='dotted')

    # Linhas radiais
    for angulo in angulos[:-1]:
        x = [0, math.cos(angulo)]
        y = [0, math.sin(angulo)]
        p.line(x, y, line_color='gray', line_dash='dotted')

    # Plotar os dados dos jogadores
    for jogador in valores_jogadores:
        valores_norm = [v / max_valor for v in jogador['valores']]
        valores_norm += valores_norm[:1]  # Fechar o gráfico

        x = [math.cos(a) * v for a, v in zip(angulos, valores_norm)]
        y = [math.sin(a) * v for a, v in zip(angulos, valores_norm)]

        source = ColumnDataSource(data=dict(
            x=x[:-1],  # Excluir o último ponto repetido
            y=y[:-1],
            atributo=atributos,
            valor=jogador['valores'],
        ))

        p.line(x, y, line_color=jogador['cor'], legend_label=jogador['nome'], line_width=2)
        p.patch(x, y, fill_color=jogador['cor'], fill_alpha=0.1)

        # Adicionar marcadores nos pontos
        pontos = p.circle('x', 'y', size=8, color=jogador['cor'], source=source)

        # Adicionar ferramenta de hover
        hover = HoverTool(tooltips=[
            ('Atributo', '@atributo'),
            ('Valor', '@valor'),
        ], renderers=[pontos])
        p.add_tools(hover)

    # Adicionar os labels dos atributos
    labels = atributos
    label_x = [math.cos(a) * 1.1 for a in angulos[:-1]]
    label_y = [math.sin(a) * 1.1 for a in angulos[:-1]]
    label_source = ColumnDataSource(data=dict(x=label_x, y=label_y, labels=labels))

    labels = LabelSet(x='x', y='y', text='labels', source=label_source,
                      text_align='center', text_baseline='middle', text_font_size='10pt')
    p.add_layout(labels)

    p.axis.visible = False
    p.grid.visible = False
    p.outline_line_color = None
    p.legend.location = "top_right"

    script, div = components(p)
    return script, div
