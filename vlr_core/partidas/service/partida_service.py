from vlr_core.partidas.repository.PartidaRepository import PartidaRepository


class PartidaService:

    @staticmethod
    def get_ultimas_partidas(time, limit=5):
        return PartidaRepository.get_ultimas_partidas(time, limit)

    @staticmethod
    def get_total_vitorias(time):
        return PartidaRepository.get_total_vitorias(time)

    @staticmethod
    def get_total_partidas(time):
        return PartidaRepository.get_total_partidas(time)
