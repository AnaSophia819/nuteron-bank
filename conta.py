from json_comandos import salvar_lista # Importar do arquivo de comandos do json a função "salvar_lista"
from procurar_cliente import cliente_existe # Importar do arquivo "procurar_cliente" a função "cliente_existe"

# Função para cadastrar conta 
def cadastrar_conta(contas, agencias, saldos, donos, cpfs):
    cpf = input("Digite o CPF do titular:")

    # Depois do cliente digitar o cpf, o código chama a função "cliente existe" para saber se esse cpf já está na lista "cpfs"
    if cliente_existe(cpf, cpfs):

        # Quando é verificado que o cliente existe no banco, ele é permitido a cadastrar uma conta
        numero_conta = input("Digite o número da conta: ")
        agencia = input("Digite a agência: ")
        saldo_inicial = float(input("Digite o saldo inicial: "))

        # Adicionando as informações da conta nas listas
        contas.append(numero_conta)
        agencias.append(agencia)
        saldos.append(saldo_inicial)
        donos.append(cpf)
        donos.append(numero_conta)

        # Chamo a função "salvar_lista" para guardar as informações digitadas
        salvar_lista("contas.json",contas)
        salvar_lista("agencias.json",agencias)
        salvar_lista("saldos.json",saldos)
        salvar_lista("donos.json",donos)

    else:
        print("Cliente não existe.")

# Busca a conta para fazer a operação
def buscar_indice_conta(conta_procurada, contas):
    for i in range(len(contas)):
        if contas[i] == conta_procurada:
            return i
    return None


def depositar(contas, saldos):
    conta_procurada =  input("Digite o numero da conta:")
    # Faz de acordo com o índice da função anterior 
    indice = buscar_indice_conta(conta_procurada, contas)

    # Se o índice (numero da conta) existir, o depoósito pode ser realizado
    if indice != None:
        valor = float(input("Digite o valor do depósito:"))
        saldos[indice] = saldos[indice] + valor
        # Salva o novo saldo na lista "saldos"
        salvar_lista("saldos.json",saldos)

    else:

        print("Conta não encontrada.")


def sacar(contas, saldos):
    conta_procurada = input("Digite o numero da conta:")
    # Faz de acordo com o índice da função anterior 
    indice = buscar_indice_conta(conta_procurada, contas)

    # Se o índice (numero da conta) existir, o saque pode ser realizado
    if indice != None:
        valor = float(input("Digite o valor do saque:"))
        # Saque só acontece se o saldo for suficiente
        if saldos[indice] >= valor:
            saldos[indice] = saldos[indice] - valor
            # Salva o novo saldo na lista "saldos"
            salvar_lista("saldos.json", saldos)
        else:
            print("Saldo insuficiente")

    else:

        print("Conta não encontrada.")

# Função para fazer conta conjunta
def adicionar_titular_extra(donos, cpfs, contas):
    cpf = input("Digite seu cpf:")
    # Procura se o cpf está na lista "cpfs#. Se tiver, faz a operação
    if cliente_existe(cpf,cpfs) is not None:
        conta = input("Numero da conta que deseja se juntar:")
        # Se a conta existir, adiciona o cpf da outra pessoa e a conta para a lista "donos"
        if buscar_indice_conta(conta, contas) is not None:
            donos.append(cpf)
            donos.append(conta)
            # Salva as informações em "donos"
            salvar_lista("donos.json",donos)
        else:
            print("Conta não encontrada.")
    else:
        print("Cliente não cadastrado")