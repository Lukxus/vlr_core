ATTRIBUTOS_DE_PARA = {
    'r_defesa': 'Rendimento na Defesa',
    'r_ataque': 'Rendimento no Ataque',
    'r_geral': 'Rendimento Geral',
    'acs_defesa': 'ACS na Defesa',
    'acs_ataque': 'ACS no Ataque',
    'acs_geral': 'ACS Geral',
    'k_defesa': 'Kills na Defesa',
    'k_ataque': 'Kills no Ataque',
    'k_geral': 'Kills Gerais',
    'd_defesa': 'Deaths na Defesa',
    'd_ataque': 'Deaths no Ataque',
    'd_geral': 'Deaths Gerais',
    'a_defesa': 'Assists na Defesa',
    'a_ataque': 'Assists no Ataque',
    'a_geral': 'Assists Gerais',
    'kda_defesa': 'KDA na Defesa',
    'kda_ataque': 'KDA no Ataque',
    'kda_geral': 'KDA Geral',
    'kast_defesa': 'KAST na Defesa',
    'kast_ataque': 'KAST no Ataque',
    'kast_geral': 'KAST Geral',
    'adr_defesa': 'ADR na Defesa',
    'adr_ataque': 'ADR no Ataque',
    'adr_geral': 'ADR Geral',
    'hs_defesa': 'Headshots na Defesa',
    'hs_ataque': 'Headshots no Ataque',
    'hs_geral': 'Headshots Gerais',
    'fk_defesa': 'First Kills na Defesa',
    'fk_ataque': 'First Kills no Ataque',
    'fk_geral': 'First Kills Gerais',
    'fd_defesa': 'First Deaths na Defesa',
    'fd_ataque': 'First Deaths no Ataque',
    'fd_geral': 'First Deaths Gerais',
    'fkfd_defesa': 'FK/FD na Defesa',
    'fkfd_ataque': 'FK/FD no Ataque',
    'fkfd_geral': 'FK/FD Geral'
}

# Listas de campos separados por categoria
CAMPOS_DEFESA = [
    'r_defesa', 'acs_defesa', 'k_defesa', 'd_defesa', 'a_defesa', 'kda_defesa',
    'kast_defesa', 'adr_defesa', 'hs_defesa', 'fk_defesa', 'fd_defesa', 'fkfd_defesa'
]

CAMPOS_ATAQUE = [
    'r_ataque', 'acs_ataque', 'k_ataque', 'd_ataque', 'a_ataque', 'kda_ataque',
    'kast_ataque', 'adr_ataque', 'hs_ataque', 'fk_ataque', 'fd_ataque', 'fkfd_ataque'
]

CAMPOS_GERAL = [
    'r_geral', 'acs_geral', 'k_geral', 'd_geral', 'a_geral', 'kda_geral',
    'kast_geral', 'adr_geral', 'hs_geral', 'fk_geral', 'fd_geral', 'fkfd_geral'
]

ATTRIBUTOS_DE_PARA = {
    'r_defesa': 'Rendimento na Defesa',
    'r_ataque': 'Rendimento no Ataque',
    'r_geral': 'Rendimento Geral',
    'acs_defesa': 'ACS na Defesa',
    'acs_ataque': 'ACS no Ataque',
    'acs_geral': 'ACS Geral',
    'k_defesa': 'Kills na Defesa',
    'k_ataque': 'Kills no Ataque',
    'k_geral': 'Kills Gerais',
    'd_defesa': 'Deaths na Defesa',
    'd_ataque': 'Deaths no Ataque',
    'd_geral': 'Deaths Gerais',
    'a_defesa': 'Assists na Defesa',
    'a_ataque': 'Assists no Ataque',
    'a_geral': 'Assists Gerais',
    'kda_defesa': 'KDA na Defesa',
    'kda_ataque': 'KDA no Ataque',
    'kda_geral': 'KDA Geral',
    'kast_defesa': 'KAST na Defesa',
    'kast_ataque': 'KAST no Ataque',
    'kast_geral': 'KAST Geral',
    'adr_defesa': 'ADR na Defesa',
    'adr_ataque': 'ADR no Ataque',
    'adr_geral': 'ADR Geral',
    'hs_defesa': 'Headshots na Defesa',
    'hs_ataque': 'Headshots no Ataque',
    'hs_geral': 'Headshots Gerais',
    'fk_defesa': 'First Kills na Defesa',
    'fk_ataque': 'First Kills no Ataque',
    'fk_geral': 'First Kills Gerais',
    'fd_defesa': 'First Deaths na Defesa',
    'fd_ataque': 'First Deaths no Ataque',
    'fd_geral': 'First Deaths Gerais',
    'fkfd_defesa': 'FK/FD na Defesa',
    'fkfd_ataque': 'FK/FD no Ataque',
    'fkfd_geral': 'FK/FD Geral'
}

# Listas auxiliares para categorias
ATRIBUTOS_DEFESA = [
    'r_defesa', 'acs_defesa', 'k_defesa', 'd_defesa', 'a_defesa',
    'kast_defesa', 'adr_defesa', 'hs_defesa',
    'fk_defesa', 'fd_defesa', 'fkfd_defesa'
]

ATRIBUTOS_ATAQUE = [
    'r_ataque', 'acs_ataque', 'k_ataque', 'd_ataque', 'a_ataque',
    'kast_ataque', 'adr_ataque', 'hs_ataque',
    'fk_ataque', 'fd_ataque', 'fkfd_ataque'
]

ATRIBUTOS_GERAL = [
    'r_geral', 'acs_geral', 'k_geral', 'd_geral', 'a_geral',
    'kast_geral', 'adr_geral', 'hs_geral',
    'fk_geral', 'fd_geral', 'fkfd_geral'
]

VALORES_MAXIMOS = {
    'r_defesa': 100,
    'r_ataque': 100,
    'r_geral': 100,
    'acs_defesa': 300,
    'acs_ataque': 300,
    'acs_geral': 300,
    'k_defesa': 30,
    'k_ataque': 30,
    'k_geral': 1000,  # Aumentando o valor máximo de k_geral para refletir melhor os dados
    'd_defesa': 30,
    'd_ataque': 30,
    'd_geral': 30,
    'a_defesa': 20,
    'a_ataque': 20,
    'a_geral': 20,
    'kda_geral': 10,
    'adr_defesa': 300,
    'adr_ataque': 300,
    'adr_geral': 300,
    'hs_defesa': 100,
    'hs_ataque': 100,
    'hs_geral': 1009,
    'fk_defesa': 10,
    'fk_ataque': 10,
    'fk_geral': 1000,
    'fd_defesa': 10,
    'fd_ataque': 10,
    'fd_geral': 1000,
    'fkfd_geral': 300,
}
