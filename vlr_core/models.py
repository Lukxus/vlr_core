from django.db import models

class Campeonato(models.Model):
    nome = models.CharField(max_length=255, db_column='nome_campeonato')
    especificacao = models.CharField(max_length=255, null=True, blank=True, db_column='especificacao_campeonato')

    class Meta:
        unique_together = ('nome', 'especificacao')
        db_table = 'campeonato'

class Time(models.Model):
    nome = models.CharField(max_length=255, unique=True, db_column='nome_time')

    class Meta:
        db_table = 'time'

class SequenciaPartida(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, db_column='id_campeonato')
    data = models.DateTimeField(db_column='data_partida')
    patch = models.CharField(max_length=255, db_column='patch_partida')
    tipo = models.IntegerField(db_column='tipo_partida')
    time1 = models.ForeignKey(Time, related_name='time1', on_delete=models.CASCADE, db_column='id_time1')
    time2 = models.ForeignKey(Time, related_name='time2', on_delete=models.CASCADE, db_column='id_time2')
    url = models.CharField(max_length=255, null=True, blank=True, db_column='url_partida')

    class Meta:
        db_table = 'sequencia_partida'

class Partida(models.Model):
    sequencia_partida = models.ForeignKey(SequenciaPartida, on_delete=models.CASCADE, db_column='id_sequencia_partida')
    mapa = models.CharField(max_length=255, db_column='mapa_partida')
    time_vencedor = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_time_vencedor')

    class Meta:
        db_table = 'partida'

class RoundsPartida(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, db_column='id_partida')
    lista_de_resultados = models.TextField(db_column='resultados_rounds')

    class Meta:
        db_table = 'rounds_partida'

class Jogador(models.Model):
    nome = models.CharField(max_length=255, db_column='nome_jogador')
    time = models.ForeignKey(Time, on_delete=models.CASCADE, db_column='id_time')

    class Meta:
        unique_together = ('nome', 'time')
        db_table = 'jogador'

class PartidaJogador(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, db_column='id_partida')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, db_column='id_jogador')
    agente = models.CharField(max_length=255, null=True, blank=True, db_column='agente_jogador')
    r_defesa = models.IntegerField(null=True, blank=True, db_column='r_defesa')
    r_ataque = models.IntegerField(null=True, blank=True, db_column='r_ataque')
    r_geral = models.IntegerField(null=True, blank=True, db_column='r_geral')
    acs_defesa = models.FloatField(null=True, blank=True, db_column='acs_defesa')
    acs_ataque = models.FloatField(null=True, blank=True, db_column='acs_ataque')
    acs_geral = models.FloatField(null=True, blank=True, db_column='acs_geral')
    k_defesa = models.IntegerField(null=True, blank=True, db_column='k_defesa')
    k_ataque = models.IntegerField(null=True, blank=True, db_column='k_ataque')
    k_geral = models.IntegerField(null=True, blank=True, db_column='k_geral')
    d_defesa = models.IntegerField(null=True, blank=True, db_column='d_defesa')
    d_ataque = models.IntegerField(null=True, blank=True, db_column='d_ataque')
    d_geral = models.IntegerField(null=True, blank=True, db_column='d_geral')
    a_defesa = models.IntegerField(null=True, blank=True, db_column='a_defesa')
    a_ataque = models.IntegerField(null=True, blank=True, db_column='a_ataque')
    a_geral = models.IntegerField(null=True, blank=True, db_column='a_geral')
    kda_defesa = models.IntegerField(null=True, blank=True, db_column='kda_defesa')
    kda_ataque = models.IntegerField(null=True, blank=True, db_column='kda_ataque')
    kda_geral = models.IntegerField(null=True, blank=True, db_column='kda_geral')
    kast_defesa = models.FloatField(null=True, blank=True, db_column='kast_defesa')
    kast_ataque = models.FloatField(null=True, blank=True, db_column='kast_ataque')
    kast_geral = models.FloatField(null=True, blank=True, db_column='kast_geral')
    adr_defesa = models.FloatField(null=True, blank=True, db_column='adr_defesa')
    adr_ataque = models.FloatField(null=True, blank=True, db_column='adr_ataque')
    adr_geral = models.FloatField(null=True, blank=True, db_column='adr_geral')
    hs_defesa = models.FloatField(null=True, blank=True, db_column='hs_defesa')
    hs_ataque = models.FloatField(null=True, blank=True, db_column='hs_ataque')
    hs_geral = models.FloatField(null=True, blank=True, db_column='hs_geral')
    fk_defesa = models.IntegerField(null=True, blank=True, db_column='fk_defesa')
    fk_ataque = models.IntegerField(null=True, blank=True, db_column='fk_ataque')
    fk_geral = models.IntegerField(null=True, blank=True, db_column='fk_geral')
    fd_defesa = models.IntegerField(null=True, blank=True, db_column='fd_defesa')
    fd_ataque = models.IntegerField(null=True, blank=True, db_column='fd_ataque')
    fd_geral = models.IntegerField(null=True, blank=True, db_column='fd_geral')
    fkfd_defesa = models.IntegerField(null=True, blank=True, db_column='fkfd_defesa')
    fkfd_ataque = models.IntegerField(null=True, blank=True, db_column='fkfd_ataque')
    fkfd_geral = models.IntegerField(null=True, blank=True, db_column='fkfd_geral')

    class Meta:
        db_table = 'partida_jogador'
