from json_comandos import salvar_lista
from procurar_cliente import cliente_existe

def cadastrar_conta(contas, agencias, saldos, donos, cpfs):
    cpf = input("Digite o CPF do titular:")

    if cliente_existe(cpf, cpfs):
        numero_conta = input()
        agencia = input()
        saldo_inicial = float(input())

        contas.append(numero_conta)
        agencias.append(agencia)
        saldos.append(saldo_inicial)
        donos.append(cpf)
        donos.append(numero_conta)

        salvar_lista("contas.json",contas)
        salvar_lista("agencias.json",agencias)
        salvar_lista("saldos.json",saldos)
        salvar_lista("donos.json",donos)

    else:
        print("Cliente não existe.")

def buscar_indice_conta(conta_procurada, contas):
    for i in range(len(contas)):
        if contas[i] == conta_procurada:
            return i

def depositar(contas, saldos):
    conta_procurada =  input("Digite o numero da conta:")
    indice = buscar_indice_conta(conta_procurada, contas)

    if indice != None:
        valor = float(input("Digite o valor do depósito:"))
        saldos[indice] = saldos[indice] + valor
        salvar_lista("saldos.json",saldos)

    else:

        print("Conta não encontrada.")

def sacar(contas, saldos):
    conta_procurada = input("Digite o numero da conta:")
    indice = buscar_indice_conta(conta_procurada, contas)

    if indice != None:
        valor = float(input("Digite o valor do saque:"))
        if saldos[indice] >= valor:
            saldos[indice] = saldos[indice] - valor
            salvar_lista("saldos.json", saldos)
        else:
            print("Saldo insuficiente")

    else:

        print("Conta não encontrada.")