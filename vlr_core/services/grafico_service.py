import matplotlib
matplotlib.use('Agg')  # Configure o backend antes de importar pyplot

import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from ..models import PartidaJogador, Jogador

class GraficoService:
    def get_grafico_context(self, request):
        atributos = [
            'r_defesa', 'r_ataque', 'r_geral', 'acs_defesa', 'acs_ataque', 'acs_geral',
            'k_defesa', 'k_ataque', 'k_geral', 'd_defesa', 'd_ataque', 'd_geral',
            'a_defesa', 'a_ataque', 'a_geral', 'kda_defesa', 'kda_ataque', 'kda_geral',
            'kast_defesa', 'kast_ataque', 'kast_geral', 'adr_defesa', 'adr_ataque',
            'adr_geral', 'hs_defesa', 'hs_ataque', 'hs_geral', 'fk_defesa', 'fk_ataque',
            'fk_geral', 'fd_defesa', 'fd_ataque', 'fd_geral', 'fkfd_defesa', 'fkfd_ataque',
            'fkfd_geral'
        ]

        if request.method == 'GET' and 'nome_jogador' in request.GET and 'atributo' in request.GET:
            nome_jogador = request.GET.get('nome_jogador').strip()
            nome_time = request.GET.get('nome_time', '').strip()
            atributo = request.GET.get('atributo')

            try:
                if nome_time:
                    jogador = Jogador.objects.get(nome__iexact=nome_jogador, time__nome__iexact=nome_time)
                    partidas_jogador = PartidaJogador.objects.filter(jogador=jogador).order_by('partida__sequencia_partida__data')
                else:
                    jogadores = Jogador.objects.filter(nome__iexact=nome_jogador)
                    partidas_jogador = PartidaJogador.objects.filter(jogador__in=jogadores).order_by('partida__sequencia_partida__data')

                datas = [partida.partida.sequencia_partida.data for partida in partidas_jogador]
                valores = [getattr(partida, atributo) for partida in partidas_jogador]

                plt.figure(figsize=(10, 5))
                plt.plot(datas, valores, marker='o')
                plt.title(f'{atributo} de {nome_jogador} {"no time " + nome_time if nome_time else "em todos os times"} ao longo do tempo')
                plt.xlabel('Data')
                plt.ylabel(atributo)
                plt.grid(True)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                uri = 'data:image/png;base64,' + urllib.parse.quote(string)

                return {
                    'grafico': uri,
                    'nome_jogador': nome_jogador,
                    'nome_time': nome_time,
                    'atributo': atributo,
                    'atributos': atributos
                }
            except Jogador.DoesNotExist:
                return {
                    'error': f'O jogador "{nome_jogador}" {"no time " + nome_time if nome_time else ""} não foi encontrado.',
                    'atributos': atributos
                }
        return {'atributos': atributos}
