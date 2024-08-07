from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Jogador, Time
from django.db.models import Q

def lista_jogadores(request):
    query = request.GET.get('q')
    team_query = request.GET.get('team')

    jogadores_list = Jogador.objects.all()

    if query:
        jogadores_list = jogadores_list.filter(Q(nome__icontains=query))

    if team_query:
        jogadores_list = jogadores_list.filter(Q(time__nome__icontains=team_query))

    paginator = Paginator(jogadores_list, 10)  # 10 jogadores por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response = {"page_obj": page_obj, "query": query, "team_query": team_query}
    return render(request, 'jogadores.html', response)
