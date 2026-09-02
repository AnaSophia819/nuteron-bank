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

    opcao = menu()

    if opcao == "1":
        cliente.cadastrar_cliente()
    elif opcao == "2":
        conta.abrir_conta()
    elif opcao == "3":
        conta.mostrar_saldo()
    elif opcao == "4":
        conta.adicionar_saldo()
    elif opcao == "5":
        conta.realizar_saque()
    elif opcao == "0":
        print("Saindo... Até logo!")
    else: 
        print("Opção inválida")

if __name__ == "__main__":
    main()

