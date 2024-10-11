from vlr_core.models import Jogador, PartidaJogador


class JogadorRepository:
    def get_all_jogadores(self):
        return Jogador.objects.all()

    def get_jogador_by_name(self, nome):
        return Jogador.objects.filter(nome=nome)

    def get_jogadores_by_team(self, nome_time):
        return Jogador.objects.filter(time__nome=nome_time)

    def get_jogador_by_name_and_team(self, nome, nome_time):
        return Jogador.objects.filter(nome=nome, time__nome=nome_time)

    def search_by_name(self, nome):
        return Jogador.objects.filter(nome__icontains=nome)

    def search_by_team(self, nome_time):
        return Jogador.objects.filter(time__nome__icontains=nome_time)

    def get_partidas_jogador(self, jogadores_ids, agente=None, atributo=None):
        query = PartidaJogador.objects.filter(jogador__id__in=jogadores_ids)
        if agente:
            query = query.filter(agente=agente)
        if atributo:
            query = query.order_by('partida__sequencia_partida__data').values_list('partida__sequencia_partida__data',
                                                                                   atributo)
        return query