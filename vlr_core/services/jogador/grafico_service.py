import matplotlib

from vlr_core.models import PartidaJogador
from vlr_core.services.jogador.atributos import ATTRIBUTOS_DE_PARA
from vlr_core.services.jogador.utils.GraficoDataFetcher import GraficoDataFetcher
from vlr_core.services.jogador.utils.GraficoGenerator import GraficoGenerator
from vlr_core.services.jogador.utils.GraficoInputValidator import GraficoInputValidator

matplotlib.use('Agg')


class GraficoService:
    def get_grafico_context(self, request):
        atributos = [key for key in ATTRIBUTOS_DE_PARA.keys()]
        atributos_amigaveis = [(key, ATTRIBUTOS_DE_PARA[key]) for key in atributos]

        # Filtrar agentes para remover valores nulos ou vazios
        agentes = PartidaJogador.objects.values_list('agente', flat=True).distinct().exclude(
            agente__isnull=True).exclude(agente__exact='')

        validator = GraficoInputValidator(request)
        is_valid, error_message = validator.is_valid()

        if not is_valid:
            return {
                'error': error_message,
                'atributos': atributos_amigaveis,
                'agentes': agentes,
            }

        nome_jogador, nome_time, agente_selecionado, atributo = validator.get_inputs()

        fetcher = GraficoDataFetcher(nome_jogador, nome_time, agente_selecionado)
        datas, partidas_jogador = fetcher.fetch_data()

        if datas is None:
            return {
                'error': f'O jogador "{nome_jogador}" {"no time " + nome_time if nome_time else ""} não foi encontrado.',
                'atributos': atributos_amigaveis,
                'agentes': agentes,
            }

        valores = [getattr(partida, atributo) for partida in partidas_jogador]

        titulo = f'{ATTRIBUTOS_DE_PARA[atributo]} de {nome_jogador} {"no time " + nome_time if nome_time else "em todos os times"}{" com o agente " + agente_selecionado if agente_selecionado else ""} ao longo do tempo'

        grafico_uri = GraficoGenerator.generate(datas, valores, titulo)

        return {
            'grafico': grafico_uri,
            'nome_jogador': nome_jogador,
            'nome_time': nome_time,
            'atributo': atributo,
            'atributos': atributos_amigaveis,
            'agentes': agentes,
            'agente_selecionado': agente_selecionado,
        }
