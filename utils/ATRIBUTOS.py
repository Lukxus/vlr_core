# Mapeamento de atributos para descrições amigáveis
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

# Listas auxiliares para categorias específicas
ATRIBUTOS_DEFESA = [
    'r_defesa', 'acs_defesa', 'k_defesa', 'd_defesa', 'a_defesa',
    'kast_defesa', 'adr_defesa', 'hs_defesa', 'fk_defesa', 'fd_defesa'
]

ATRIBUTOS_ATAQUE = [
    'r_ataque', 'acs_ataque', 'k_ataque', 'd_ataque', 'a_ataque',
    'kast_ataque', 'adr_ataque', 'hs_ataque', 'fk_ataque', 'fd_ataque'
]

ATRIBUTOS_GERAL = [
    'r_geral', 'acs_geral', 'k_geral', 'd_geral', 'a_geral',
    'kast_geral', 'adr_geral', 'hs_geral', 'fk_geral', 'fd_geral'
]

# Valores máximos por atributo
VALORES_MAXIMOS = {
    'r_defesa': 5, 'r_ataque': 5, 'r_geral': 5,
    'acs_defesa': 5, 'acs_ataque': 5, 'acs_geral': 5,
    'k_defesa': 40, 'k_ataque': 40, 'k_geral': 40,
    'd_defesa': 40, 'd_ataque': 40, 'd_geral': 40,
    'a_defesa': 10, 'a_ataque': 10, 'a_geral': 10,
    'kda_defesa': 10, 'kda_ataque': 10, 'kda_geral': 10,
    'adr_defesa': 5, 'adr_ataque': 5, 'adr_geral': 5,
    'hs_defesa': 40, 'hs_ataque': 40, 'hs_geral': 40,
    'fk_defesa': 5, 'fk_ataque': 5, 'fk_geral': 5,
    'fd_defesa': 5, 'fd_ataque': 5, 'fd_geral': 5,
    'fkfd_geral': 40
}

# Atributos globais
ATRIBUTOS = ['acs', 'kda', 'adr', 'hs', 'kast', 'fk', 'r', 'k', 'd', 'a']

# Valores mínimos e máximos globais
VALORES_MINIMOS = {
    'acs': 0, 'kda': 0, 'adr': 0, 'hs': 0, 'kast': 0, 'fk': 0,
    'r': 0, 'k': 0, 'd': 0, 'a': 0
}

VALORES_MAXIMOS_GLOBAIS = {
    'acs': 300, 'kda': 5, 'adr': 200, 'hs': 100, 'kast': 100, 'fk': 20,
    'r': 5, 'k': 40, 'd': 40, 'a': 20
}

# Mapeamento de labels para gráficos
LABELS_MAPPING = {
    'acs': 'ACS', 'kda': 'KDA', 'adr': 'ADR', 'hs': 'HS%',
    'kast': 'KAST%', 'fk': 'First Kills', 'r': 'Rendimento',
    'k': 'Kills', 'd': 'Deaths', 'a': 'Assists'
}
