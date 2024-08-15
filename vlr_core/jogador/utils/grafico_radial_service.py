import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse

from utils.ATRIBUTOS import ATTRIBUTOS_DE_PARA
from vlr_core.jogador.repository.jogador_repository import JogadorRepository


class GraficoRadialService:

    @staticmethod
    def get_grafico_radial(jogador_nome, categoria):
        estatisticas_medias = JogadorRepository.get_estatisticas_jogador_por_nome(jogador_nome, categoria)
        print(f"Estatísticas médias para {jogador_nome} ({categoria}): {estatisticas_medias}")  # Debug
        if estatisticas_medias:
            atributos_filtrados = {key: value for key, value in estatisticas_medias.items() if value is not None}
            print(f"Atributos filtrados: {atributos_filtrados}")  # Debug
            if atributos_filtrados:
                return GraficoRadialService.gerar_grafico_radial(atributos_filtrados)
        return None

    @staticmethod
    def gerar_grafico_radial(estatisticas):
        labels = [ATTRIBUTOS_DE_PARA[key] for key in estatisticas.keys()]
        stats = list(estatisticas.values())

        print(f"Labels: {labels}")  # Debug
        print(f"Stats: {stats}")  # Debug

        stats_normalizados = []
        for key, valor in estatisticas.items():
            max_valor = max(estatisticas.values())
            if max_valor != 0:
                stats_normalizados.append(valor / max_valor)
            else:
                stats_normalizados.append(0)

        print(f"Stats normalizados: {stats_normalizados}")  # Debug

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
