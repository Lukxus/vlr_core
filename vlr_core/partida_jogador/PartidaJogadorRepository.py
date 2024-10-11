from vlr_core.models import PartidaJogador
from django.db.models import Q

class PartidaJogadorRepository:
    def get_all_agentes(self):
        """
        Retorna todos os agentes distintos da base de dados.
        """
        return PartidaJogador.objects.values_list('agente', flat=True).distinct()

    def get_atributo_by_jogador(self, jogador_id, atributo):
        """
        Retorna o valor de um atributo específico para um jogador.
        """
        # Certifica-se de que o atributo é um campo válido antes de fazer a consulta
        if hasattr(PartidaJogador, atributo):
            return PartidaJogador.objects.filter(jogador_id=jogador_id).values_list(atributo, flat=True)
        else:
            raise ValueError(f"O atributo '{atributo}' não é válido para a entidade PartidaJogador.")

    def search_by_agente(self, jogadores_ids, agente):
        """
        Retorna partidas filtradas por agente para uma lista de IDs de jogadores.
        """
        return PartidaJogador.objects.filter(Q(jogador__id__in=jogadores_ids) & Q(agente=agente))

    def search_by_atributo(self, jogadores_ids, atributo):
        """
        Retorna partidas filtradas por um atributo específico para uma lista de IDs de jogadores.
        """
        if hasattr(PartidaJogador, atributo):
            return PartidaJogador.objects.filter(jogador__id__in=jogadores_ids).only(atributo)
        else:
            raise ValueError(f"O atributo '{atributo}' não é válido para a entidade PartidaJogador.")

    def get_partidas_jogador(self, jogadores_ids, agente=None, atributo=None):
        query = PartidaJogador.objects.filter(jogador__id__in=jogadores_ids)
        if agente:
            query = query.filter(agente=agente)
        if atributo:
            query = query.order_by('partida__sequencia_partida__data').values_list('partida__sequencia_partida__data',
                                                                                   atributo)
        return query
