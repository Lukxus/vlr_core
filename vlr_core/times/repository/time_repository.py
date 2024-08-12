from vlr_core.models import Time

class TimeRepository:

    @staticmethod
    def get_times(query=None):
        times_list = Time.objects.all().order_by('nome')

        if query:
            times_list = times_list.filter(nome__icontains=query)

        return times_list

    @staticmethod
    def get_top_10_times_com_mais_vitorias():
        return Time.objects.order_by('-vitorias')[:10]
