from django.core.paginator import Paginator
from django.db.models import Avg

from vlr_core.jogador.JogadorRepository import JogadorRepository
from vlr_core.models import Jogador, PartidaJogador
from vlr_core.partida_jogador.PartidaJogadorService import PartidaJogadorService


class JogadorService:
    def __init__(self):
        self.repository = JogadorRepository()
        self.partida_jogador_service = PartidaJogadorService()

    def listar_jogadores(self, nome=None, nome_time=None, page=1, page_size=10):
        """
        Lista jogadores com filtros opcionais para nome e time.
        Paginação é aplicada com base nos parâmetros page e page_size.
        """
        if nome:
            jogadores = self.repository.search_by_name(nome)
        elif nome_time:
            jogadores = self.repository.search_by_team(nome_time)
        else:
            jogadores = self.repository.get_all_jogadores()

        paginator = Paginator(jogadores.order_by('nome'), page_size)
        return paginator.get_page(page)

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
        """
        Lista todos os agentes disponíveis na base de dados.
        """
        return self.partida_jogador_service.listar_agentes()

    def obter_dados_para_comparacao(self, nome_jogador, categoria):
        try:
            jogadores = Jogador.objects.filter(nome=nome_jogador)
            if not jogadores.exists():
                return None

            atributos = ['acs', 'kda', 'adr', 'hs', 'kast']
            dados = {}

            for atributo in atributos:
                campo = f"{atributo}_{categoria}"
                # Obter todas as partidas dos jogadores com o nome fornecido
                partidas_jogador = PartidaJogador.objects.filter(jogador__in=jogadores)
                # Calcular a média do atributo nas partidas
                media = partidas_jogador.aggregate(media_atributo=Avg(campo))['media_atributo']
                if media is not None:
                    dados[atributo.upper()] = media
                else:
                    dados[atributo.upper()] = 0  # Trate conforme necessário

            return dados
        except Exception as e:
            print(f"Erro ao obter dados para comparação: {e}")
            return None


