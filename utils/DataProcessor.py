from django.db.models import Q

from vlr_core.models import Jogador


class DataProcessor:
    @staticmethod
    def search_by_player_name(query):
        return Jogador.objects.filter(Q(nome__icontains=query))

    @staticmethod
    def search_by_team_name(team_query):
        return Jogador.objects.filter(Q(time__nome__icontains=team_query))
