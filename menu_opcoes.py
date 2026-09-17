import cliente
import conta
from json_comandos import carregar_lista 


def mostrar_menu():
    print("""
======= NUTERON BANK =======

[1] Cadastrar cliente
[2] Criar conta
[3] Consultar saldo
[4] Realizar depósito
[5] Realizar saque
[6] Adicionar titular à conta
[0] Sair
""")

    return input("Escolha uma opção: ").strip()

def carregar_dados():
    global nomes, cpfs, contas, agencias, saldos, donos

    nomes = carregar_lista("nomes.json")
    cpfs = carregar_lista("cpfs.json")
    contas = carregar_lista("contas.json")
    agencias = carregar_lista("agencias.json")
    saldos = carregar_lista("saldos.json")
    donos = carregar_lista("donos.json")

def main():
    carregar_dados()

    opcao = ""
    while opcao != "0":
        opcao = mostrar_menu()

        if opcao == "1":
            cliente.cadastrar(cpfs, nomes)
        elif opcao == "2":
            conta.cadastrar_conta(contas, agencias, saldos, donos, cpfs)
            
        elif opcao == "3":
            conta_procurada = input("Digite o número da conta: ")
            indice = conta.buscar_indice_conta(conta_procurada, contas)
            if indice is not None:
                print(f"Saldo da conta {contas[indice]}: R$ {saldos[indice]:.2f}")
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            conta.depositar(contas, saldos)
        elif opcao == "5":
            conta.sacar(contas, saldos)
        elif opcao == "6":
            conta.adicionar_titular_extra(contas, donos, cpfs)
        elif opcao == "0":
            print("Desligando...")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()