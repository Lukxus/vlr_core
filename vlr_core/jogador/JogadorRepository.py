from vlr_core.models import Jogador


class JogadorRepository:
    def get_all_jogadores(self):
        return Jogador.objects.all()

    def get_jogador_by_name(self, nome):
        return Jogador.objects.filter(nome=nome)

    def get_jogadores_by_team(self, nome_time):
        return Jogador.objects.filter(time__nome=nome_time)

    def get_jogador_by_name_and_team(self, nome, nome_time):
        return Jogador.objects.filter(nome=nome, time__nome=nome_time)
