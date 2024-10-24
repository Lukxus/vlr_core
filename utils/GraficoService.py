import math

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.palettes import Category10
from bokeh.plotting import figure

from utils.ATRIBUTOS import LABELS_MAPPING, ATRIBUTOS, VALORES_MAXIMOS_GLOBAIS


class GraficoService:

    @staticmethod
    def gerar_grafico_radial(dados_jogador1, dados_jogador2, nome_jogador1, nome_jogador2, categoria):
        # Usar os atributos e valores do arquivo de configuração
        atributos_full = ATRIBUTOS

        # Construir o título com base nos nomes dos jogadores e na categoria
        if nome_jogador1 and nome_jogador2:
            titulo = f"Comparação de Atributos: {nome_jogador1} vs {nome_jogador2} - Categoria: {categoria.capitalize()}"
        elif nome_jogador1:
            titulo = f"Atributos de {nome_jogador1} - Categoria: {categoria.capitalize()}"
        elif nome_jogador2:
            titulo = f"Atributos de {nome_jogador2} - Categoria: {categoria.capitalize()}"
        else:
            titulo = f"Comparação de Atributos - Categoria: {categoria.capitalize()}"

        # Preparar o gráfico
        p = figure(title=titulo, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2),
                   toolbar_location=None, tools="")

        p.toolbar.logo = None

        # Desenhar linhas de grade circulares
        num_circulos = 5
        circulos = [i / num_circulos for i in range(1, num_circulos + 1)]
        for radius in circulos:
            p.annulus(x=0, y=0, inner_radius=0, outer_radius=radius, fill_color=None, line_color='gray',
                      line_dash='dotted', line_width=0.5)

        # Linhas radiais
        angulos = [n / float(len(atributos_full)) * 2 * math.pi for n in range(len(atributos_full))]
        angulos += angulos[:1]  # Fechar o gráfico

        for angulo in angulos[:-1]:
            x = [0, math.cos(angulo)]
            y = [0, math.sin(angulo)]
            p.line(x, y, line_color='gray', line_dash='dotted', line_width=0.5)

        # Função para processar dados de cada jogador
        def processar_jogador(jogador_dados, jogador_nome, cor):
            if jogador_dados:
                valores_norm = []
                valores_originais = []
                for attr in atributos_full:
                    valor = jogador_dados.get(attr, 0.00) or 0.00

                    valor_max = VALORES_MAXIMOS_GLOBAIS.get(attr, 1.00)

                    # Normalização min-max
                    valor_normalizado = valor / valor_max
                    valores_norm.append(valor_normalizado)
                    valores_originais.append(valor)

                valores_norm += valores_norm[:1]  # Fechar o gráfico

                x = [math.cos(a) * v for a, v in zip(angulos, valores_norm)]
                y = [math.sin(a) * v for a, v in zip(angulos, valores_norm)]

                source = ColumnDataSource(data=dict(
                    x=x[:-1],
                    y=y[:-1],
                    atributo=[attr.upper() for attr in atributos_full],
                    valor=valores_originais,
                ))

                p.line(x, y, line_color=cor, legend_label=jogador_nome, line_width=2)
                p.patch(x, y, fill_color=cor, fill_alpha=0.2)

                # Adicionar marcadores nos pontos
                pontos = p.scatter('x', 'y', size=6, color=cor, source=source, marker="circle")

                # Adicionar ferramenta de hover
                hover = HoverTool(tooltips=[
                    ('Atributo', '@atributo'),
                    ('Valor', '@valor{0.00}'),
                ], renderers=[pontos])
                p.add_tools(hover)

        # Paleta de cores
        cores = Category10[10]

        # Processar cada jogador
        processar_jogador(dados_jogador1, nome_jogador1, cores[0])
        processar_jogador(dados_jogador2, nome_jogador2, cores[1])

        # Adicionar os labels dos atributos
        labels_attrs = [LABELS_MAPPING.get(attr, attr.upper()) for attr in atributos_full]
        label_x = [math.cos(a) * 1.05 for a in angulos[:-1]]
        label_y = [math.sin(a) * 1.05 for a in angulos[:-1]]
        label_source = ColumnDataSource(data=dict(x=label_x, y=label_y, labels=labels_attrs))

        labels = LabelSet(x='x', y='y', text='labels', source=label_source,
                          text_align='center', text_baseline='middle', text_font_size='9pt')
        p.add_layout(labels)

        p.axis.visible = False
        p.grid.visible = False
        p.outline_line_color = None
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"

        script, div = components(p)
        return script, div
