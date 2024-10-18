from django.db.models import Count, Q, F

from vlr_core.models import Time, Partida

class TimeRepository:
    def get_all_times(self):
        return Time.objects.all()

    def search_by_name(self, nome):
        return Time.objects.filter(nome__icontains=nome)

    def get_top_teams_by_wins(self, limit=20):
        return (
            Time.objects.annotate(vitorias=Count('partida', filter=Q(partida__time_vencedor=F('id'))))
            .order_by('-vitorias')[:limit]
        )

    def get_partidas_por_time(self, time_id):
        return Partida.objects.filter(
            sequencia_partida__time1_id=time_id
        ) | Partida.objects.filter(
            sequencia_partida__time2_id=time_id
        )