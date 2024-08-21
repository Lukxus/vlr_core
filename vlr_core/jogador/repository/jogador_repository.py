from django.db.models import Avg
from django.forms import FloatField, IntegerField

from vlr_core import models
from vlr_core.jogador.atributos import CAMPOS_DEFESA, CAMPOS_ATAQUE, CAMPOS_GERAL
from vlr_core.models import Jogador, PartidaJogador


class JogadorRepository:

    @staticmethod
    def get_jogadores(query=None, team_query=None):
        jogadores_list = Jogador.objects.all().order_by('nome')

        if query:
            jogadores_list = jogadores_list.filter(nome__icontains=query)

        if team_query:
            jogadores_list = jogadores_list.filter(time__nome__icontains=team_query)

        return jogadores_list

    @staticmethod
    def get_jogador_por_nome(nome):
        return Jogador.objects.filter(nome__iexact=nome)

    @staticmethod
    def get_estatisticas_jogador_por_nome(jogador_nome, categoria):
        jogadores = Jogador.objects.filter(nome__iexact=jogador_nome)
        if not jogadores.exists():
            return None

        # Escolhe a lista de campos com base na categoria
        if categoria == 'defesa':
            campos = CAMPOS_DEFESA
        elif categoria == 'ataque':
            campos = CAMPOS_ATAQUE
        else:  # 'geral' ou qualquer outro valor
            campos = CAMPOS_GERAL

        # Cria o dicionário de agregação com base nos campos filtrados
        fields_to_aggregate = {
            campo: Avg(campo) for campo in campos
        }

        # Agrega as estatísticas para todos os registros dos jogadores encontrados
        estatisticas = PartidaJogador.objects.filter(jogador__in=jogadores).aggregate(**fields_to_aggregate)
        print(f"Estatísticas agregadas: {estatisticas}")  # Debug

        # Substitui None por 0 nos valores do dicionário de estatísticas
        estatisticas = {campo: valor if valor is not None else 0 for campo, valor in estatisticas.items()}

        return estatisticas
