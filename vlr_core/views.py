from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .services.grafico_service import GraficoService
from .services.jogadores_service import JogadoresService


class HomeView(TemplateView):
    template_name = "home.html"


class ListaJogadoresView(ListView):
    template_name = "jogadores.html"
    context_object_name = "page_obj"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        team_query = self.request.GET.get('team')
        return JogadoresService.get_jogadores(query, team_query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['team_query'] = self.request.GET.get('team', '')
        context['paginate_by'] = self.request.GET.get('paginate_by', 10)
        return context


def grafico_atributo(request):
    service = GraficoService()
    context = service.get_grafico_context(request)
    return render(request, 'grafico_atributo.html', context)
