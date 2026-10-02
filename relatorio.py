# 1. Contas por CPF
def relatorio_contas_por_cpf(contas):
    print("\n========== CONTAS POR CPF ==========")
    contagem = {}
    for i in contas:
        cpf = i.get("CPF")
        contagem[cpf] = contagem.get(cpf, 0) + 1

    for cpf, quantidade in contagem.items():
        print(f"CPF: {cpf} | Quantidade de contas: {quantidade}")


# 2. Contas por agência
def relatorio_contas_por_agencia(contas):
    print("\n========== CONTAS POR AGÊNCIA ==========")

    contagem = {}
    for i in contas:
        agencia = i.get("Agencia")
        contagem[agencia] = contagem.get(agencia, 0) + 1
    for agencia, quantidade in contagem.items():
        print(f"Agência: {agencia} | Quantidade de contas: {quantidade}")


# 3. Contas com mais de um dono
def relatorio_contas_multiplos_donos(contas):
    print("\n========== CONTAS COM MAIS DE UM DONO ==========")

            
    for i in contas:
        if "Titulares extras" in i:
            print(f"Conta: {i.get("Numero da conta")} | Agência: {i.get("Agencia")} | Saldo: R$ {i.get("Saldo", 0):.2f} | Quantidade de donos: {1 + len(i.get("Titulares extras", []))} | CPFs: {i.get("CPF")}, {', '.join([titular.get("cpf") for titular in i.get("Titulares extras", [])])}")

        else:
            print(f"{i.get("Numero da conta")}: Não possui mais de um dono.")


# 4. Saldo por cliente
def relatorio_saldo_por_cliente(contas):
    print("\n========== SALDO POR CLIENTE ==========")

    contagem = {}
    for i in contas:
        cpf = i.get("CPF")
        saldo = i.get("Saldo", 0)
        contagem[cpf] = contagem.get(cpf, 0) + saldo

    for cpf, saldo in contagem.items():
        print(f"CPF: {cpf} | Saldo total: R$ {saldo:.2f}")


# 5. Relatório geral
def relatorio_geral(contas):
    print("\n========== RELATÓRIO GERAL ==========")

    contagem = {}
    for i in contas:
        aux = i.get("Saldo", 0)

        contagem["saldo_total"] = contagem.get("saldo_total", 0) + aux
        contagem["quantidade_contas"] = contagem.get("quantidade_contas", 0) + 1
        contagem["quantidade_clientes"] = len(set([i.get("CPF") for i in contas]))
        contagem["quantidade_agencias"] = len(set([i.get("Agencia") for i in contas]))

    print(f"Quantidade de contas: {contagem.get('quantidade_contas', 0)}")
    print(f"Quantidade de clientes: {contagem.get('quantidade_clientes', 0)}")
    print(f"Saldo total do banco: R$ {contagem.get('saldo_total', 0):.2f}")
    print(f"Quantidade de agências: {contagem.get('quantidade_agencias', 0)}")


# Lista todos os clientes do banco
def listar_clientes(contas):
    print("\n========== LISTA DE CLIENTES ==========")
    for i in contas:
        cpf = i.get("CPF")
        nome = i.get("Nome")
        print(f"Nome: {nome} | CPF: {cpf}")

# Saldo por agência, entrega o total de saldo de cada agência
def saldo_por_agencia(contas):
    contagem = {}
    for i in contas:
        agencia = i.get("Agencia")
        saldo = i.get("Saldo", 0)
        contagem[agencia] = contagem.get(agencia, 0) + saldo

    print("\n========== SALDO POR AGÊNCIA ==========")
    for n, m in contagem.items():
        print(f"Agência: {n} | Saldo total: R$ {m:.2f}")


# Lista todas as contas do banco, com agência e saldo. Isso cobre, ao mesmo tempo, as funções de listar agências e contas Obs: não mostra os titulares das contas
def listar_contas(contas):
    print("\n========== LISTA DE CONTAS ==========")
    for i in contas:
        agencia = i.get("Agencia")
        numero_conta = i.get("Numero da conta")
        saldo = i.get("Saldo", 0)
        print(f"Agência: {agencia} | Conta: {numero_conta} | Saldo: R$ {saldo:.2f}")
    