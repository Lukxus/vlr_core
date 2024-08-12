from vlr_core.models import Partida

class PartidaRepository:

    @staticmethod
    def get_ultimas_partidas(time, limit=5):
        return Partida.objects.filter(sequencia_partida__time1=time).order_by('-sequencia_partida__data')[:limit]

    @staticmethod
    def get_total_vitorias(time):
        return Partida.objects.filter(sequencia_partida__time1=time, time_vencedor=time).count()

    @staticmethod
    def get_total_partidas(time):
        return Partida.objects.filter(sequencia_partida__time1=time).count()
