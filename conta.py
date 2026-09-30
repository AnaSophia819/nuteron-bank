from json_comandos import salvar_lista # Importar do arquivo de comandos do json a função "salvar_lista"
from cliente import cadastrar # Importar do arquivo "cliente" a função "cadastrar"

# Função para cadastrar conta 
def cadastrar_conta(contas):
    cpf, nome = cadastrar(contas) #Chama a função "cadastrar" do arquivo "cliente.py" para cadastrar o cliente
    if cpf is None:
        return
    
    conta = {} # Cria um dicionário para armazenar as informações da conta
    numero_conta = input("Digite o número da conta: ").strip()
    agencia = input("Digite a agência: ").strip()
    saldo_inicial = float(input("Digite o saldo inicial: ").strip())
    tipo = input("Dige o tipo da conta (Corrente, Salário ou Poupança): ").strip()
    # Adicionando as informações da conta no dicionário
    conta["Numero da conta"] = numero_conta
    conta["Agencia"] = agencia
    conta["Saldo"] = saldo_inicial
    conta["CPF"] = cpf
    conta["Nome"] = nome
    conta["Tipo"] = tipo
    contas.append(conta) # Adiciona o dicionário da conta na lista de contas
    
    # Chamo a função "salvar_lista" para guardar as informações digitadas
    salvar_lista("contas.json",contas)

# Busca a conta para fazer a operação
def buscar_indice_conta(conta_procurada, contas):
    contador = 0
    for i in contas:
        if i.get("Numero da conta") == conta_procurada:
            return contador
        contador +=1
    return None


def depositar(contas):
    conta_procurada =  input("Digite o numero da conta:").strip()
    # Faz de acordo com o índice da função anterior 
    indice = buscar_indice_conta(conta_procurada, contas)

    # Se o índice (numero da conta) existir, o depoósito pode ser realizado
    if indice != None:
        valor = float(input("Digite o valor do depósito:").strip())
        contas[indice]["Saldo"] = contas[indice].get("Saldo") + valor
        # Salva o novo saldo na lista "contas"
        salvar_lista("contas.json",contas)

    else:

        print("Conta não encontrada.")


def sacar(contas):
    conta_procurada = input("Digite o numero da conta:").strip()
    # Faz de acordo com o índice da função anterior 
    indice = buscar_indice_conta(conta_procurada, contas)

    # Se o índice (numero da conta) existir, o saque pode ser realizado
    if indice != None:
        valor = float(input("Digite o valor do saque:").strip())
        # Saque só acontece se o saldo for suficiente
        if contas[indice].get("Saldo") >= valor:
            contas[indice]["Saldo"] = contas[indice].get("Saldo") - valor
            # Salva o novo saldo na lista "saldos"
            salvar_lista("contas.json",contas)
        else:
            print("Saldo insuficiente")
    else:
        print("Conta não encontrada.")

# Função para fazer conta conjunta
def adicionar_titular_extra(contas):
    cpf, nome = cadastrar(contas)
    if cpf is None:
        return
    
    conta = input("Numero da conta que deseja se juntar:").strip()
    indice = buscar_indice_conta(conta, contas)

    contas[indice].setdefault("Titulares extras", [])
    contas[indice]["Titulares extras"].append({"Nome": nome, "cpf": cpf})
    salvar_lista("contas.json", contas)

def listar_saldo(contas):
    conta_procurada = input("Digite o número da conta:").strip()
    indice = buscar_indice_conta(conta_procurada, contas)
    if indice is not None:
        print(f"Saldo da conta {conta_procurada}: R${contas[indice].get("Saldo")}")
    else:
        print("Conta não encontrada")
