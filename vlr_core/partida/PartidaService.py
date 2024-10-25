from collections import Counter

from vlr_core.partida.PartidaRepository import PartidaRepository


class PartidaService:
    def __init__(self):
        self.repository = PartidaRepository()

    def contar_partidas(self):
        return self.repository.contar_partidas()

    def contar_partidas_por_mes(self):
        partidas = self.repository.obter_partidas_com_sequencia()
        meses = [partida.sequencia_partida.data.strftime('%Y-%m') for partida in partidas]
        partidas_por_mes = Counter(meses)
        partidas_por_mes_ordenado = sorted(partidas_por_mes.items())

        return partidas_por_mes_ordenado


