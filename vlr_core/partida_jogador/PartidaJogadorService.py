from vlr_core.partida_jogador.PartidaJogadorRepository import PartidaJogadorRepository

class PartidaJogadorService:
    def __init__(self):
        self.repository = PartidaJogadorRepository()

    def buscar_partidas_jogador(self, jogadores_ids, agente=None, atributo=None):
        query = self.repository.get_partidas_jogador(jogadores_ids, agente=agente, atributo=atributo)
        return query

    def listar_agentes(self):
        """
        Retorna todos os agentes distintos na base de dados.
        """
        return self.repository.get_all_agentes()

    def buscar_atributo_jogador(self, jogador_id, atributo):
        """
        Retorna o valor de um atributo específico para um jogador.
        """
        return self.repository.get_atributo_by_jogador(jogador_id, atributo)
