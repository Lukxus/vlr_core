import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, CDSView, BooleanFilter
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.transform import factor_cmap
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from sklearn.cluster import KMeans

from utils.ATRIBUTOS import ATTRIBUTOS_DE_PARA
from utils.GraficoService import GraficoService
from vlr_core.campeonato.CampeonatoService import CampeonatoService
from vlr_core.jogador.JogadorService import JogadorService
from vlr_core.partida.PartidaService import PartidaService
from vlr_core.times.TimeService import TimeService


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jogadorService = JogadorService()
        quantidade_total_jogadores = jogadorService.contar_jogadore()

        partidaService = PartidaService()
        quantidade_total_partidas = partidaService.contar_partidas()

        campeonatoService = CampeonatoService()
        quantidade_total_campeonatos = campeonatoService.contar_campeonatos()

        context['quantidade_total_jogadores'] = quantidade_total_jogadores
        context['quantidade_total_partidas'] = quantidade_total_partidas
        context['quantidade_total_campeonatos'] = quantidade_total_campeonatos

        partidas_por_mes = partidaService.contar_partidas_por_mes()
        meses, quantidades = zip(*partidas_por_mes)
        p = figure(x_range=meses, title="Quantidade de partidas por mês na base de dados", height=250, width=2000, background_fill_color="#2c2c2c")
        p.vbar(x=meses, top=quantidades, width=0.6, color="#7B20E2")
        hover = HoverTool()
        hover.tooltips = [("Mês", "@x"), ("Quantidade", "@top")]
        p.add_tools(hover)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_text_font_size = '0pt'  # Remove as legendas do eixo X
        p.title.text_color = "white"  # Cor do título
        p.xaxis.axis_label_text_color = "white"
        p.yaxis.axis_label_text_color = "white"
        p.yaxis.major_label_text_color = "white"  # Cor dos labels do eixo Y
        p.border_fill_color = "#2c2c2c"  # Fundo em torno do gráfico
        script, div = components(p)
        context['bokeh_script_partidas'] = script
        context['bokeh_div_partidas'] = div

        return context


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
                # Filtrar valores None
                dados_filtrados = [(data, valor) for data, valor in dados if valor is not None]

                if dados_filtrados:
                    # Usar índices sequenciais para o eixo x e garantir que os dados estejam ordenados por data
                    indices = np.arange(len(dados_filtrados))
                    valores = [valor for _, valor in dados_filtrados]

                    # Criar o ColumnDataSource
                    source = ColumnDataSource(data=dict(
                        x=indices,
                        y=valores,
                        data=[data for data, _ in dados_filtrados]  # Manter a data para exibição no hover
                    ))

                    # Construir o título com base nos filtros
                    titulo = f"Evolução de {atributo} para {nome}"
                    if nome_time:
                        titulo += f" - Time: {nome_time}"
                    if agente:
                        titulo += f" - Agente: {agente}"

                    p = figure(x_axis_label="Partidas (ordenadas por data)", title=titulo, height=350, width=800,
                               background_fill_color="#2c2c2c", border_fill_color="#2c2c2c")

                    p.line('x', 'y', source=source, line_width=2, line_color="#7B20E2")
                    p.scatter('x', 'y', marker="circle", size=8, source=source, fill_color="#7B20E2",
                              line_color="purple")

                    # Modificar a cor dos eixos e outros elementos visuais para melhor visibilidade em fundo preto
                    p.xaxis.axis_label_text_color = "white"
                    p.yaxis.axis_label_text_color = "white"
                    p.xaxis.major_label_text_color = "white"
                    p.yaxis.major_label_text_color = "white"
                    p.title.text_color = "white"

                    hover = HoverTool(tooltips=[
                        ("Data", "@data{%F}"),
                        (f"Valor de {atributo}", "@y")
                    ], formatters={'@data': 'datetime'})
                    p.add_tools(hover)

                    script, div = components(p)
                    context['bokeh_script'] = script
                    context['bokeh_div'] = div
                else:
                    context['error_message'] = "Nenhum dado disponível para exibição após aplicar os filtros."
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
        categoria = request.POST.get('categoria', 'geral').strip()

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
        script, div = GraficoService.gerar_grafico_radial(
            dados_jogador1, dados_jogador2,
            jogador1_nome if dados_jogador1 else None,
            jogador2_nome if dados_jogador2 else None,
            categoria
        )

        bokeh_resources = CDN.render()

        context = {
            'bokeh_script': script,
            'bokeh_div': div,
            'bokeh_resources': bokeh_resources,
            'jogador1_nome': jogador1_nome,
            'jogador2_nome': jogador2_nome,
            'categoria': categoria,  # Adicionando a categoria ao contexto
        }
        return render(request, self.template_name, context)

class ClusterizacaoView(View):
    template_name = 'clusterizacao.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        jogador_nome = request.POST.get('jogador', '').strip()
        time_nome = request.POST.get('time', '').strip()

        # Verificar se ao menos um dos campos foi preenchido
        if not jogador_nome and not time_nome:
            context = {'error_message': 'Por favor, preencha pelo menos um dos campos.'}
            return render(request, self.template_name, context)

        # Obter os dados usando o JogadorService
        jogador_service = JogadorService()
        dados_query = jogador_service.obter_dados_jogador_clusterizacao()

        # Convertendo o QuerySet para DataFrame
        dados = pd.DataFrame(list(dados_query))

        # Verificar se o DataFrame está vazio
        if dados.empty:
            context = {'error_message': 'Nenhum dado encontrado para os filtros aplicados.'}
            return render(request, self.template_name, context)

        # Nome do jogador para destacar
        jogador_destacado = jogador_nome if jogador_nome else None

        # Lista para armazenar os gráficos de cada ano
        graficos_por_ano = []

        # Agrupar o DataFrame por ano
        for ano, grupo in dados.groupby('ano'):
            # Selecionar as colunas numéricas para a clusterização
            x = grupo[['kda_media', 'acs_media']]

            # Verificar se o grupo possui amostras suficientes para o número de clusters
            if len(grupo) < 4:
                # Se não houver amostras suficientes, pular este ano
                continue

            # Criar o modelo KMeans com o número desejado de clusters (ex: 4 clusters)
            kmeans = KMeans(n_clusters=4)
            kmeans.fit(x)

            # Adicionar o cluster de cada jogador ao DataFrame
            grupo['Cluster'] = kmeans.labels_.astype(str)

            # Verificar se o jogador de interesse está presente neste ano
            grupo['is_destacado'] = grupo['jogador__nome'] == jogador_destacado if jogador_destacado else False

            # Obter os centroides dos clusters
            centroides = kmeans.cluster_centers_

            # Criar fontes de dados para os gráficos e para os centroides
            source = ColumnDataSource(grupo)
            centroid_source = ColumnDataSource(data=dict(
                kda=centroides[:, 0],
                acs=centroides[:, 1]
            ))

            # Criar uma view para o jogador destacado
            view_destacado = CDSView(source=source, filters=[BooleanFilter(grupo['is_destacado'])])

            # Criar o gráfico de scatter plot para esse ano
            p = figure(title=f"Clusterização - Ano {int(ano)}",
                       x_axis_label="KDA Média",
                       y_axis_label="ACS Média",
                       tools="pan,wheel_zoom,box_zoom,reset,hover",
                       tooltips=[("Jogador", "@jogador__nome"), ("KDA Média", "@kda_media"),
                                 ("ACS Média", "@acs_media")])

            # Adicionar os pontos dos jogadores coloridos pelos clusters
            p.scatter('kda_media', 'acs_media', source=source, size=8,
                      color=factor_cmap('Cluster', palette=Spectral4, factors=grupo['Cluster'].unique()),
                      legend_field='Cluster')

            # Adicionar os centroides como 'x' pretos
            p.scatter('kda', 'acs', source=centroid_source, size=15, color='black', marker='x',
                      legend_label='Centroides')

            # Adicionar destaque para o jogador específico usando a view
            if jogador_destacado:
                p.scatter('kda_media', 'acs_media', source=source, size=12, color='purple',
                          legend_label=f'{jogador_destacado}', view=view_destacado)

            # Adicionar o gráfico à lista
            graficos_por_ano.append(p)

        # Organizar os gráficos lado a lado
        grid = gridplot(graficos_por_ano, ncols=2)  # Ajuste ncols conforme o número de gráficos e espaço

        # Renderizar o template com o gráfico
        context = {
            'jogador_nome': jogador_nome,
            'time_nome': time_nome,
            'graficos': grid,
            'dados_jogador': dados
        }
        return render(request, self.template_name, context)


class PredicaoView(View):
    template_name = 'predicao_vencedor.html'

    def get(self, request):
        return render(request, self.template_name)




