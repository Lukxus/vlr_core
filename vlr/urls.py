from django.contrib import admin
from django.urls import path

from vlr_core.views import grafico_atributo, HomeView, ListaJogadoresView, ListaTimesView, TimeDetalhesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('jogadores/', ListaJogadoresView.as_view(), name='lista_jogadores'),
    path('grafico/', grafico_atributo, name='grafico_atributo'),
    path('times/', ListaTimesView.as_view(), name='lista_times'),
    path('times/<int:pk>/', TimeDetalhesView.as_view(), name='detalhes_time'),  # Altere o name para "detalhes_time"
]
