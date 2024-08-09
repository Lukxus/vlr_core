class GraficoInputValidator:
    def __init__(self, request):
        self.request = request
        self.nome_jogador = self.request.GET.get('nome_jogador', '').strip()
        self.nome_time = self.request.GET.get('nome_time', '').strip()
        self.agente_selecionado = self.request.GET.get('agente', '').strip()
        self.atributo = self.request.GET.get('atributo')

    def is_valid(self):
        if not self.nome_jogador:
            return False, 'O nome do jogador é obrigatório.'
        if not self.atributo:
            return False, 'O atributo é obrigatório.'
        return True, None

    def get_inputs(self):
        return self.nome_jogador, self.nome_time, self.agente_selecionado, self.atributo
