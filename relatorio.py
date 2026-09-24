def buscar_titulares(conta_procurada, donos):
    titulares = []

    for i in range(0, len(donos), 2):
        cpf = donos[i]
        conta = donos[i + 1]

        if conta == conta_procurada:
            titulares.append(cpf)

    return titulares


# 1. Contas por CPF
def relatorio_contas_por_cpf(cpfs, donos):
    print("\n========== CONTAS POR CPF ==========")

    for cpf in cpfs:
        quantidade = 0

        for i in range(0, len(donos), 2):
            cpf_dono = donos[i]

            if cpf_dono == cpf:
                quantidade += 1

        print(f"CPF: {cpf} | Quantidade de contas: {quantidade}")


# 2. Contas por agência
def relatorio_contas_por_agencia(contas, agencias):
    print("\n========== CONTAS POR AGÊNCIA ==========")

    agencias_encontradas = []

    for agencia in agencias:
        if agencia not in agencias_encontradas:
            agencias_encontradas.append(agencia)

    for agencia in agencias_encontradas:
        quantidade = 0

        for agencia_conta in agencias:
            if agencia_conta == agencia:
                quantidade += 1

        print(f"Agência: {agencia} | Quantidade de contas: {quantidade}")


# 3. Contas com mais de um dono
def relatorio_contas_multiplos_donos(contas, donos):
    print("\n========== CONTAS COM MAIS DE UM DONO ==========")

    encontrou = False

    for conta in contas:
        titulares = buscar_titulares(conta, donos)

        if len(titulares) > 1:
            encontrou = True
            print(f"Conta: {conta}")
            print(f"Quantidade de donos: {len(titulares)}")
            print(f"CPFs: {', '.join(titulares)}")
            print()

    if not encontrou:
        print("Nenhuma conta possui mais de um dono.")


# 4. Saldo por cliente
def relatorio_saldo_por_cliente(cpfs, donos, contas, saldos):
    print("\n========== SALDO POR CLIENTE ==========")

    for cpf in cpfs:
        saldo_cliente = 0

        for i in range(0, len(donos), 2):
            cpf_dono = donos[i]
            numero_conta = donos[i + 1]

            if cpf_dono == cpf:
                indice = buscar_indice_conta(numero_conta, contas)

                if indice is not None:
                    saldo_cliente += saldos[indice]

        print(f"CPF: {cpf} | Saldo total: R$ {saldo_cliente:.2f}")


# Função auxiliar para encontrar o índice da conta
def buscar_indice_conta(conta_procurada, contas):
    for i in range(len(contas)):
        if contas[i] == conta_procurada:
            return i

    return None


# 5. Relatório geral
def relatorio_geral(contas, agencias, saldos, cpfs):
    print("\n========== RELATÓRIO GERAL ==========")

    quantidade_contas = len(contas)
    quantidade_clientes = len(cpfs)
    saldo_total = sum(saldos)
    quantidade_agencias = len(set(agencias))

    print(f"Quantidade de contas: {quantidade_contas}")
    print(f"Quantidade de clientes: {quantidade_clientes}")
    print(f"Saldo total do banco: R$ {saldo_total:.2f}")
    print(f"Quantidade de agências: {quantidade_agencias}")