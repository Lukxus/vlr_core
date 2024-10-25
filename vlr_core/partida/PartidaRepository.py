from vlr_core.models import Partida


class PartidaRepository:
    def contar_partidas(self):
        return Partida.objects.count()

    def obter_partidas_com_sequencia(self):
        return Partida.objects.select_related('sequencia_partida').all()
