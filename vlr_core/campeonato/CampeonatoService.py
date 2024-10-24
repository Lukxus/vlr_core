from django.core.paginator import Paginator
from django.db.models import Avg

from vlr_core.campeonato.CampeonatoRepository import CampeonatoRepository
from vlr_core.jogador.JogadorRepository import JogadorRepository
from vlr_core.models import Jogador, PartidaJogador
from vlr_core.partida_jogador.PartidaJogadorService import PartidaJogadorService


class CampeonatoService:
    def __init__(self):
        self.repository = CampeonatoRepository()


    def contar_campeonatos(self):
        return self.repository.contar_campeonatos()





