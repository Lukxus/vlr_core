from ..models import Jogador

class JogadoresService:
    @staticmethod
    def get_jogadores(query=None, team_query=None):
        jogadores_list = Jogador.objects.all().order_by('nome')

        if query:
            jogadores_list = jogadores_list.filter(nome__icontains=query)

        if team_query:
            jogadores_list = jogadores_list.filter(time__nome__icontains=team_query)

        return jogadores_list
