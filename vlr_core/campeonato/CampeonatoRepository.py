from vlr_core.models import Campeonato


class CampeonatoRepository:
    def contar_campeonatos(self):
        return Campeonato.objects.values("nome").distinct().count()
