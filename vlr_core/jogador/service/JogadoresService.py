from vlr_core.repositories.jogador_repository import JogadorRepository
from vlr_core.jogador.atributos import ATTRIBUTOS_DE_PARA

class JogadoresService:

    @staticmethod
    def get_jogadores(query=None, team_query=None):
        return JogadorRepository.get_jogadores(query, team_query)

    @staticmethod
    def get_estatisticas_jogador_por_nome(nome):
        jogadores = JogadorRepository.get_jogador_por_nome(nome)

        if not jogadores.exists():
            return None

        estatisticas_totais = {key: 0 for key in ATTRIBUTOS_DE_PARA.keys()}

        for jogador in jogadores:
            for atributo in estatisticas_totais.keys():
                valor = getattr(jogador, atributo, 0)
                estatisticas_totais[atributo] += valor

        num_jogadores = jogadores.count()
        estatisticas_medias = {key: valor / num_jogadores for key, valor in estatisticas_totais.items()}

        return estatisticas_medias
