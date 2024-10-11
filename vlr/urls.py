from django.contrib import admin
from django.urls import path

from vlr_core.views import (
    HomeView, ListaJogadoresView, GraficoAtributoView, ListaTimesView, DetalhesTimeView,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('jogadores/', ListaJogadoresView.as_view(), name='lista_jogadores'),
    path('grafico/', GraficoAtributoView.as_view(), name='grafico_atributo'),
    path('times/', ListaTimesView.as_view(), name='lista_times'),
    path('times/<int:id>/', DetalhesTimeView.as_view(), name='detalhes_time'),
]

