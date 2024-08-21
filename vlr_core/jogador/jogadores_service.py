from vlr_core.models import Jogador
from vlr_core.jogador.atributos import ATTRIBUTOS_DE_PARA


class JogadoresService:

    @staticmethod
    def get_jogadores(query=None, team_query=None):
        jogadores_list = Jogador.objects.all().order_by('nome')

        if query:
            jogadores_list = jogadores_list.filter(nome__icontains=query)

        if team_query:
            jogadores_list = jogadores_list.filter(time__nome__icontains=team_query)

        return jogadores_list

    @staticmethod
    def get_estatisticas_jogador_por_nome(nome):
        try:
            jogador = Jogador.objects.get(nome__iexact=nome)  # Busca pelo nome exato (case-insensitive)
            # Supondo que as estatísticas são armazenadas como atributos do modelo Jogador
            return [
                jogador.estatistica1,  # Exemplo de estatísticas
                jogador.estatistica2,
                jogador.estatistica3,
                jogador.estatistica4
            ]
        except Jogador.DoesNotExist:
            return None

    @staticmethod
    def get_estatisticas_jogador_por_nome(nome):
        jogadores = Jogador.objects.filter(nome__iexact=nome)

        if not jogadores.exists():
            return None

        # Inicializa um dicionário para somar as estatísticas
        estatisticas_totais = {key: 0 for key in ATTRIBUTOS_DE_PARA.keys()}

        # Itera sobre todos os registros encontrados e soma as estatísticas
        for jogador in jogadores:
            for atributo in estatisticas_totais.keys():
                valor = getattr(jogador, atributo, 0)  # Pega o valor do atributo ou 0 se não existir
                estatisticas_totais[atributo] += valor

        # Calcula a média das estatísticas
        num_jogadores = jogadores.count()
        estatisticas_medias = {key: valor / num_jogadores for key, valor in estatisticas_totais.items()}

        return estatisticas_medias
