from django.db.models import Max

from vlr_core.jogador.atributos import ATTRIBUTOS_DE_PARA
from vlr_core.jogador.repository.jogador_repository import JogadorRepository
from vlr_core.models import PartidaJogador


class JogadoresService:

    @staticmethod
    def get_jogadores(query=None, team_query=None):
        return JogadorRepository.get_jogadores(query, team_query)

    @staticmethod
    def get_estatisticas_jogador_por_nome(nome):
        jogadores = JogadorRepository.get_jogador_por_nome(nome)

        if not jogadores.exists():
            return None

        estatisticas_totais = {key: 0 for key in ATTRIBUTOS_DE_PARA.keys()}

        for jogador in jogadores:
            for atributo in estatisticas_totais.keys():
                valor = getattr(jogador, atributo, 0)
                estatisticas_totais[atributo] += valor

        num_jogadores = jogadores.count()
        estatisticas_medias = {key: valor / num_jogadores for key, valor in estatisticas_totais.items()}

        return estatisticas_medias

    @staticmethod
    def get_media_estatisticas_jogador_por_nome(nome, categoria):
        estats = JogadorRepository.get_estatisticas_jogador_por_nome(nome, categoria)
        estats = JogadoresService.remover_chaves_fkfd(estats)
        return estats

    @staticmethod
    def remover_chaves_fkfd(dicionario):
        if dicionario is None:
            return None

        # Cria uma lista de chaves para remover
        chaves_para_remover = [chave for chave in dicionario if (chave.upper()).startswith('KAST') or (chave.upper()).startswith('FKFD')]

        # Remove as chaves do dicionário
        for chave in chaves_para_remover:
            del dicionario[chave]

        return dicionario

    @staticmethod
    def obter_valores_maximos():
        return PartidaJogador.objects.aggregate(
            r_defesa=Max('r_defesa'),
            r_ataque=Max('r_ataque'),
            r_geral=Max('r_geral'),
            acs_defesa=Max('acs_defesa'),
            acs_ataque=Max('acs_ataque'),
            acs_geral=Max('acs_geral'),
            k_defesa=Max('k_defesa'),
            k_ataque=Max('k_ataque'),
            k_geral=Max('k_geral'),
            d_defesa=Max('d_defesa'),
            d_ataque=Max('d_ataque'),
            d_geral=Max('d_geral'),
            a_defesa=Max('a_defesa'),
            a_ataque=Max('a_ataque'),
            a_geral=Max('a_geral'),
            kda_defesa=Max('kda_defesa'),
            kda_ataque=Max('kda_ataque'),
            kda_geral=Max('kda_geral'),
            kast_defesa=Max('kast_defesa'),
            kast_ataque=Max('kast_ataque'),
            kast_geral=Max('kast_geral'),
            adr_defesa=Max('adr_defesa'),
            adr_ataque=Max('adr_ataque'),
            adr_geral=Max('adr_geral'),
            hs_defesa=Max('hs_defesa'),
            hs_ataque=Max('hs_ataque'),
            hs_geral=Max('hs_geral'),
            fk_defesa=Max('fk_defesa'),
            fk_ataque=Max('fk_ataque'),
            fk_geral=Max('fk_geral'),
            fd_defesa=Max('fd_defesa'),
            fd_ataque=Max('fd_ataque'),
            fd_geral=Max('fd_geral'),
            fkfd_defesa=Max('fkfd_defesa'),
            fkfd_ataque=Max('fkfd_ataque'),
            fkfd_geral=Max('fkfd_geral'),
        )
