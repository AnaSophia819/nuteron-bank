from conta import ContaSalario, ContaPoupanca

class Cliente():

    # Construtor do cliente
    def __init__(self, nome, cpf, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.contas_cliente = []

    # Atualizar cadastro do cliente
    def atualizarcadastro(self, nome, cpf, telefone, email):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

    def adicionarconta(self, conta):
        self.contas_cliente.append(conta)

    