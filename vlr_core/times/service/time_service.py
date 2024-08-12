from django.core.paginator import Paginator
from django.db.models import Count, Q, F

from vlr_core.times.repository.time_repository import TimeRepository


class TimeService:

    @staticmethod
    def get_times(query=None):
        return TimeRepository.get_times(query).annotate(
            vitorias=Count('partida', filter=Q(partida__time_vencedor=F('id')))
        ).order_by('-vitorias')

    @staticmethod
    def paginate_times(times_list, paginate_by, page):
        paginator = Paginator(times_list, paginate_by)
        return paginator.get_page(page)

    @staticmethod
    def get_top_10_times_com_mais_vitorias():
        return TimeRepository.get_top_10_times_com_mais_vitorias()
