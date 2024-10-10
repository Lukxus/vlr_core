from django.core.paginator import Paginator

from vlr_core.jogador.JogadorRepository import JogadorRepository
from vlr_core.partida_jogador.PartidaJogadorService import PartidaJogadorService


class JogadorService:
    def __init__(self):
        self.repository = JogadorRepository()
        self.partida_jogador_service = PartidaJogadorService()

    def buscar_dados_para_grafico(self, nome, atributo, nome_time=None, agente=None):
        if nome_time:
            jogadores = self.repository.get_jogador_by_name_and_team(nome, nome_time)
        else:
            jogadores = self.repository.get_jogador_by_name(nome)

        if not jogadores.exists():
            return None

        # Coletar todos os IDs dos jogadores correspondentes
        jogadores_ids = jogadores.values_list('id', flat=True)

        # Passar todos os IDs para o método buscar_partidas_jogador
        dados = self.partida_jogador_service.buscar_partidas_jogador(jogadores_ids, agente=agente, atributo=atributo)
        return dados if dados else None

    def listar_agentes(self):
        return self.partida_jogador_service.listar_agentes()

    def listar_jogadores(self, nome=None, nome_time=None, page=1, page_size=10):
        if nome:
            jogadores = self.repository.search_by_name(nome)
        elif nome_time:
            jogadores = self.repository.search_by_team(nome_time)
        else:
            jogadores = self.repository.get_all_jogadores()

        paginator = Paginator(jogadores, page_size)
        return paginator.get_page(page)

    def buscar_atributo(self, nome_jogador, nome_time, atributo):
        if not nome_jogador or not nome_time or not atributo:
            return []

        # Busca exata pelos dados
        return self.repository.get_atributo_data(nome_jogador, nome_time, atributo)
