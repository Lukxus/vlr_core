from vlr_core.models import Partida


class PartidaRepository:
    def contar_partidas(self):
        return Partida.objects.count()
