# vlr_core/services/partida_jogador_service.py
from vlr_core.partida_jogador.PartidaJogadorRepository import PartidaJogadorRepository


class PartidaJogadorService:
    def __init__(self):
        self.repository = PartidaJogadorRepository()

    def buscar_partidas_jogador(self, jogadores_ids, agente=None, atributo=None):
        query = self.repository.get_partidas_jogador(jogadores_ids, agente=agente, atributo=atributo)
        return query

    def listar_agentes(self):
        return self.repository.get_all_agentes()
