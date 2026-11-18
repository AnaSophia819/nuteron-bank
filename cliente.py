class Cliente():
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def cadastrar(self, nome, cpf):
        """Cadastra um novo cliente"""
        self.nome = nome
        self.cpf = cpf