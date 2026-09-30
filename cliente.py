from procurar_cliente import cliente_existe
from procurar_cliente import buscar_indice
# Função para cadastrar clientes
def cadastrar(contas):
    cpf = input("Digite seu CPF:").strip()

    if not cliente_existe(contas, cpf):
        nome = input("Digite seu nome:").strip()
        print("Cliente cadastrado com sucesso!")
    else:
        nome = buscar_indice(contas, cpf)["Nome"]
        print("Cliente já cadastrado!")

    return cpf, nome