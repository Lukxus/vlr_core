from vlr_core.models import Jogador

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
