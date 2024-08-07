from django.db import models

class Campeonato(models.Model):
    nome = models.CharField(max_length=255)
    especificacao = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('nome', 'especificacao')
        db_table = 'campeonato'

class Time(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'time'

class SequenciaPartida(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    data = models.DateTimeField()
    patch = models.CharField(max_length=255)
    tipo = models.IntegerField()
    Id_time1 = models.ForeignKey(Time, related_name='time1', on_delete=models.CASCADE)
    time2 = models.ForeignKey(Time, related_name='time2', on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'sequencia_partida'

class Partida(models.Model):
    sequencia_partida = models.ForeignKey(SequenciaPartida, on_delete=models.CASCADE)
    mapa = models.CharField(max_length=255)
    time_vencedor = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'partida'

class RoundsPartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    lista_de_resultados = models.TextField()

    class Meta:
        db_table = 'rounds_partida'

class Jogador(models.Model):
    nome = models.CharField(max_length=255)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nome', 'time')
        db_table = 'jogador'

class PartidaJogador(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    agente = models.CharField(max_length=255, null=True, blank=True)
    r_defesa = models.IntegerField(null=True, blank=True)
    r_ataque = models.IntegerField(null=True, blank=True)
    r_geral = models.IntegerField(null=True, blank=True)
    acs_defesa = models.FloatField(null=True, blank=True)
    acs_ataque = models.FloatField(null=True, blank=True)
    acs_geral = models.FloatField(null=True, blank=True)
    k_defesa = models.IntegerField(null=True, blank=True)
    k_ataque = models.IntegerField(null=True, blank=True)
    k_geral = models.IntegerField(null=True, blank=True)
    d_defesa = models.IntegerField(null=True, blank=True)
    d_ataque = models.IntegerField(null=True, blank=True)
    d_geral = models.IntegerField(null=True, blank=True)
    a_defesa = models.IntegerField(null=True, blank=True)
    a_ataque = models.IntegerField(null=True, blank=True)
    a_geral = models.IntegerField(null=True, blank=True)
    kda_defesa = models.IntegerField(null=True, blank=True)
    kda_ataque = models.IntegerField(null=True, blank=True)
    kda_geral = models.IntegerField(null=True, blank=True)
    kast_defesa = models.FloatField(null=True, blank=True)
    kast_ataque = models.FloatField(null=True, blank=True)
    kast_geral = models.FloatField(null=True, blank=True)
    adr_defesa = models.FloatField(null=True, blank=True)
    adr_ataque = models.FloatField(null=True, blank=True)
    adr_geral = models.FloatField(null=True, blank=True)
    hs_defesa = models.FloatField(null=True, blank=True)
    hs_ataque = models.FloatField(null=True, blank=True)
    hs_geral = models.FloatField(null=True, blank=True)
    fk_defesa = models.IntegerField(null=True, blank=True)
    fk_ataque = models.IntegerField(null=True, blank=True)
    fk_geral = models.IntegerField(null=True, blank=True)
    fd_defesa = models.IntegerField(null=True, blank=True)
    fd_ataque = models.IntegerField(null=True, blank=True)
    fd_geral = models.IntegerField(null=True, blank=True)
    fkfd_defesa = models.IntegerField(null=True, blank=True)
    fkfd_ataque = models.IntegerField(null=True, blank=True)
    fkfd_geral = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'partida_jogador'
