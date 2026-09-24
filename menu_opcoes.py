import cliente
import conta
import relatorio
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
[7] Relatórios
[0] Sair
""")

    return input("Escolha uma opção: ").strip()

def mostrar_menu_relatorios():
    print("""
======= RELATÓRIOS =======
[1] Contas por CPF
[2] Contas por agência
[3] Contas com mais de um dono
[4] Saldo por cliente
[5] Saldo total por agência
[6] Listar clientes
[7] Listar contas
[8] Relatório geral
[0] Voltar
""")
    return input("Escolha uma opção: ").strip()


def menu_retalorios():
    opcao = ""
    while opcao != "0":
        opcao = mostrar_menu_relatorios()

        if opcao == "1":
            relatorio.relatorio_contas_por_cpf(cpfs, donos)
        elif opcao == "2":
            relatorio.relatorio_contas_por_agencia(contas, agencias)
        elif opcao == "3":
            relatorio.relatorio_contas_multiplos_donos(contas, donos)
        elif opcao == "4":
            relatorio.relatorio_saldo_por_cliente(cpfs, donos, contas, saldos)
        elif opcao == "5":
            relatorio.saldo_por_agencia(agencias, saldos)
        elif opcao == "6":
            relatorio.listar_clientes(cpfs, nomes)
        elif opcao == "7":
            relatorio.listar_contas(contas, agencias, saldos)
        elif opcao == "8":
            relatorio.relatorio_geral(contas, agencias, saldos, cpfs)
        elif opcao == "0":
            print("Voltando ao menu principal...")
        else:
            print("Opção inválida. Tente novamente.")
    main()

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
            conta.adicionar_titular_extra(donos, cpfs, contas)
        elif opcao == "7":
            menu_retalorios()
        elif opcao == "0":
            print("Desligando...")
        else:
            print("Opção inválida. Tente novamente.")