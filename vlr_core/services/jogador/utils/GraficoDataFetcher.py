from vlr_core.models import Jogador, PartidaJogador


class GraficoDataFetcher:
    def __init__(self, nome_jogador, nome_time, agente_selecionado):
        self.nome_jogador = nome_jogador
        self.nome_time = nome_time
        self.agente_selecionado = agente_selecionado

    def fetch_data(self):
        try:
            if self.nome_time:
                jogador = Jogador.objects.get(nome__iexact=self.nome_jogador, time__nome__iexact=self.nome_time)
                partidas_jogador = PartidaJogador.objects.filter(jogador=jogador)
            else:
                jogadores = Jogador.objects.filter(nome__iexact=self.nome_jogador)
                partidas_jogador = PartidaJogador.objects.filter(jogador__in=jogadores)

            if self.agente_selecionado:
                partidas_jogador = partidas_jogador.filter(agente__iexact=self.agente_selecionado)

            partidas_jogador = partidas_jogador.order_by('partida__sequencia_partida__data')

            datas = [partida.partida.sequencia_partida.data for partida in partidas_jogador]
            return datas, partidas_jogador

        except Jogador.DoesNotExist:
            return None, None
