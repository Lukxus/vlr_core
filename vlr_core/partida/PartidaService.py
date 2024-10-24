from vlr_core.partida.PartidaRepository import PartidaRepository


class PartidaService:
    def __init__(self):
        self.repository = PartidaRepository()

    def contar_partidas(self):
        return self.repository.contar_partidas()


