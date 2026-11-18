import cliente
import conta
import relatorio
from json_comandos import carregar_lista 


def mostrar_menu():
    print("""
======= NUTERON BANK =======

[1] Criar conta
[2] Consultar saldo
[3] Realizar depósito
[4] Realizar saque
[5] Adicionar titular à conta
[6] Relatórios
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
            relatorio.relatorio_contas_por_cpf(contas)
        elif opcao == "2":
            relatorio.relatorio_contas_por_agencia(contas)
        elif opcao == "3":
            relatorio.relatorio_contas_multiplos_donos(contas)
        elif opcao == "4":
            relatorio.relatorio_saldo_por_cliente(contas)
        elif opcao == "5":
            relatorio.saldo_por_agencia(contas)
        elif opcao == "6":
            relatorio.listar_clientes(contas)
        elif opcao == "7":
            relatorio.listar_contas(contas)
        elif opcao == "8":
            relatorio.relatorio_geral(contas)
        elif opcao == "0":
            print("Voltando ao menu principal...")
        else:
            print("Opção inválida. Tente novamente.")
    main()

def carregar_dados():
    global contas
    contas = carregar_lista("contas.json")

def main():
    carregar_dados()

    opcao = ""
    while opcao != "0":
        opcao = mostrar_menu()

        if opcao == "1":
            conta.cadastrar_conta(contas)
        elif opcao == "2":
            conta.listar_saldo(conta)
        elif opcao == "3":
            conta.depositar(contas)
        elif opcao == "4":
            conta.sacar(contas)
        elif opcao == "5":
            conta.adicionar_titular_extra(contas)
        elif opcao == "6":
            menu_retalorios()
        elif opcao == "0":
            print("Desligando...")
        else:
            print("Opção inválida. Tente novamente.")
