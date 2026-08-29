def adicionar_nome():
    nome = input("Digite o nome do cliente: ")
    print(f"Cliente {nome} adicionado com sucesso!")
    return nome

def adicionar_cpf():
    cpf = input("Digite o CPF do cliente: ")
    print(f"CPF {cpf} adicionado com sucesso!")
    return cpf

def cadastrar_cliente(): #Essa função abaixo já retornar os dois parametros com uma única chamada, as duas funções acima fazem a mesma coisa, mas de forma separada.
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o CPF do cliente: ")
    print(f"Cliente {nome} com CPF {cpf} cadastrado com sucesso!")
    return nome, cpf

def abrir_conta():
    saldo = 0.0
    return saldo
