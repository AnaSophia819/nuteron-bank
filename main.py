import cliente
import conta

def menu():

    print("=======MENU======= \n"
    "[1] para cadastrar cliente \n" 
    " [2] para criar uma conta \n"
    " [3] para consultar saldo \n"
    " [4] para realizar depósito \n"
    " [5] para realizar saque \n"
    " [0] para sair")

    resposta = input("Digite aqui:")

    return resposta

def main():
    saldo_conta = 0.0

    while True:
        opcao = menu()

        if opcao == "1":

            cliente.cadastrar_cliente()

        elif opcao == "2":

            saldo_conta = conta.abrir_conta()

        elif opcao == "3":

            conta.mostrar_saldo(saldo_conta)

        elif opcao == "4":

            saldo_conta = conta.adicionar_saldo(saldo_conta)
            
        elif opcao == "5":

            saldo_conta = conta.realizar_saque(saldo_conta)

        elif opcao == "0":

            print("Saindo... Até logo!")
            break

        else:

            print("Opção inválida")

if __name__ == "__main__":
    main()

