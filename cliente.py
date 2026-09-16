from procurar_cliente import cliente_existe
from json_comandos import salvar_lista

def cadastrar(cpfs, nomes):
    cpf = input("Digite seu CPF:")

    if not cliente_existe(cpf, cpfs):

        cpfs.append(cpf)
        nome = input("Digite seu nome:")
        nomes.append(nome)

        salvar_lista("cpfs.json", cpfs)
        salvar_lista("nomes.json", nomes)
        print("Cliente cadastrado com sucesso!")
    else:
        print("Cliente já cadastrado!")