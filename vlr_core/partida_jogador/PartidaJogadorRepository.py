from vlr_core.models import PartidaJogador

class PartidaJogadorRepository:
    def get_partidas_jogador(self, jogadores_ids, agente=None, atributo=None):
        query = PartidaJogador.objects.filter(jogador__id__in=jogadores_ids)
        if agente:
            query = query.filter(agente=agente)
        if atributo:
            query = query.order_by('partida__sequencia_partida__data').values_list('partida__sequencia_partida__data', atributo)
        return query

    def get_all_agentes(self):
        return PartidaJogador.objects.values_list('agente', flat=True).distinct()
