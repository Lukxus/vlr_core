import base64
import io
import urllib.parse

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils.ATRIBUTOS import ATTRIBUTOS_DE_PARA
from vlr_core.jogador.atributos import VALORES_MAXIMOS
from vlr_core.jogador.service.JogadoresService import JogadoresService


class GraficoRadialService:

    @staticmethod
    def normalizar_estatisticas(stats, labels):
        stats_normalizados = []
        for stat, label in zip(stats, labels):
            atributo_original = [key for key, value in ATTRIBUTOS_DE_PARA.items() if value == label][0]
            max_valor = VALORES_MAXIMOS.get(atributo_original)

            stat_normalizado = stat / max_valor

            stats_normalizados.append(stat_normalizado)

        return stats_normalizados

    @staticmethod
    def get_grafico_radial(jogador_nome_1, jogador_nome_2, categoria):
        estatisticas_1 = JogadoresService.get_media_estatisticas_jogador_por_nome(jogador_nome_1, categoria)
        estatisticas_2 = None
        if jogador_nome_2:
            estatisticas_2 = JogadoresService.get_media_estatisticas_jogador_por_nome(jogador_nome_2, categoria)

        if not estatisticas_1:
            return None

        atributos_filtrados_1 = GraficoRadialService.filtrar_atributos(estatisticas_1)
        atributos_filtrados_2 = GraficoRadialService.filtrar_atributos(estatisticas_2) if estatisticas_2 else None

        return GraficoRadialService.gerar_grafico_radial(atributos_filtrados_1, atributos_filtrados_2, jogador_nome_1,
                                                         jogador_nome_2)

    @staticmethod
    def filtrar_atributos(estatisticas):
        return {key: value for key, value in estatisticas.items() if value is not None and value >= 0}

    @staticmethod
    def escalar(dicionario):
        if dicionario is None:
            if dicionario is None:
                return None

        for chave in dicionario.keys():
            if chave.upper().startswith('ACS') or chave.upper().startswith('ADR'):
                dicionario[chave] = dicionario[chave] / 100

        return dicionario

    @staticmethod
    def gerar_grafico_radial(estatisticas_1, estatisticas_2=None, nome_1=None, nome_2=None):
        labels, stats_1, stats_reais_1 = GraficoRadialService.preparar_dados_para_grafico(estatisticas_1)
        stats_1 = GraficoRadialService.normalizar_estatisticas(
            list(GraficoRadialService.escalar(estatisticas_1).values()), labels)

        stats_2 = None
        stats_reais_2 = None
        if estatisticas_2:
            _, stats_2, stats_reais_2 = GraficoRadialService.preparar_dados_para_grafico(estatisticas_2)
            stats_2 = GraficoRadialService.normalizar_estatisticas(
                list(GraficoRadialService.escalar(estatisticas_2).values()), labels)

        angles = GraficoRadialService.calcular_angulos(len(labels))
        stats_1 += stats_1[:1]
        stats_reais_1 += stats_reais_1[:1]
        angles += angles[:1]

        if stats_2:
            stats_2 += stats_2[:1]
            stats_reais_2 += stats_reais_2[:1]

        fig, ax = GraficoRadialService.configurar_plot(angles, stats_1, stats_2)

        GraficoRadialService.configurar_labels(ax, angles, labels)
        GraficoRadialService.plotar_valores(ax, angles, stats_1, stats_reais_1, color='blue', label=nome_1)
        if stats_2:
            GraficoRadialService.plotar_valores(ax, angles, stats_2, stats_reais_2, color='red', label=nome_2)

        return GraficoRadialService.renderizar_grafico(fig)

    @staticmethod
    def preparar_dados_para_grafico(estatisticas):
        labels = [ATTRIBUTOS_DE_PARA[key] for key in estatisticas.keys()]
        stats = list(estatisticas.values())
        return labels, stats, stats

    @staticmethod
    def calcular_angulos(num_labels):
        return np.linspace(0, 2 * np.pi, num_labels, endpoint=False).tolist()

    @staticmethod
    def configurar_plot(angles, stats_1, stats_2=None):
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        color_1 = sns.color_palette("coolwarm", n_colors=2)[0]
        color_2 = sns.color_palette("coolwarm", n_colors=2)[1] if stats_2 is not None else color_1

        ax.fill(angles, stats_1, color=color_1, alpha=0.4)
        ax.plot(angles, stats_1, color=color_1, linewidth=2)

        if stats_2 is not None:
            ax.fill(angles, stats_2, color=color_2, alpha=0.4)
            ax.plot(angles, stats_2, color=color_2, linewidth=2)

        ax.set_ylim(0, 1)
        ax.spines['polar'].set_visible(False)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)

        return fig, ax

    @staticmethod
    def configurar_labels(ax, angles, labels):
        ax.set_rlabel_position(0)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=12, color='darkblue', fontweight='bold')

        # Remover os números ao longo da linha radial
        ax.set_yticklabels([])

    @staticmethod
    def plotar_valores(ax, angles, stats_normalizados, stats_reais, color, label=None):
        ax.fill(angles, stats_normalizados, color=color, alpha=0.4)
        ax.plot(angles, stats_normalizados, color=color, linewidth=2, label=label)
        for angle, stat_normalizado, stat_real in zip(angles[:-1], stats_normalizados[:-1], stats_reais[:-1]):
            ax.text(angle, stat_normalizado + 0.05, f'{stat_real:.2f}', color=color, ha='center', va='center',
                    fontsize=10)

        if label:
            ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    @staticmethod
    def renderizar_grafico(fig):
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        return 'data:image/png;base64,' + urllib.parse.quote(string)
