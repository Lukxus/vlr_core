from django.core.paginator import Paginator
from django.db.models import Count, Q, F

from vlr_core.models import Time


class TimeService:

    @staticmethod
    def get_times(query):
        times = Time.objects.all()
        if query:
            times = times.filter(nome__icontains=query)
        return times.order_by('nome')

    @staticmethod
    def paginate_times(times, paginate_by, page):
        paginator = Paginator(times, paginate_by)
        return paginator.get_page(page)

    @staticmethod
    def get_top_10_times_com_mais_vitorias():
        return (Time.objects
                .annotate(vitorias=Count('partida', filter=Q(partida__time_vencedor=F('id'))))
                .order_by('-vitorias')[:10])
