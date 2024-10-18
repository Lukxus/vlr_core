from django.core.paginator import Paginator
from vlr_core.times.TimeRepository import TimeRepository

class TimeService:
    def __init__(self):
        self.repository = TimeRepository()

    def listar_times(self, nome=None, page=1, page_size=10):
        if nome:
            times = self.repository.search_by_name(nome).order_by('nome')
        else:
            times = self.repository.get_all_times().order_by('nome')

        paginator = Paginator(times, page_size)
        return paginator.get_page(page)

    def listar_top_times_por_vitorias(self, limit=20):
        return self.repository.get_top_teams_by_wins(limit)

    def listar_partidas_por_time(self, time_id, page=1, page_size=10):
        partidas = self.repository.get_partidas_por_time(time_id).order_by('-sequencia_partida__data')

        # Contadores de vitórias e derrotas
        total_vitorias = 0
        total_derrotas = 0

        partidas_com_resultado = []
        for partida in partidas:
            if partida.time_vencedor_id == time_id:
                resultado = 'Vitória'
                total_vitorias += 1
            else:
                resultado = 'Derrota'
                total_derrotas += 1

            partidas_com_resultado.append({
                'partida': partida,
                'resultado': resultado
            })

        paginator = Paginator(partidas_com_resultado, page_size)
        paginated_partidas = paginator.get_page(page)

        return {
            'partidas': paginated_partidas,
            'total_vitorias': total_vitorias,
            'total_derrotas': total_derrotas
        }
