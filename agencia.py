class Agencia:

    def __init__(self, numero, nome, endereco):
        self.numero = numero
        self.nome = nome
        self.endereco = endereco
        self.clientes = []

    def adicionarCliente(self, cliente):
        self.clientes.append(cliente)

    def getCliente(self):
        return self.clientes
    
