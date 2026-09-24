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


# Lista todos os clientes do banco
def listar_clientes(cpfs, nomes):
    print("\n========== LISTA DE CLIENTES ==========")
    for i in range(len(cpfs)):
        print(f"Nome: {nomes[i]} | CPF: {cpfs[i]}")


# Saldo por agência, entrega o total de saldo de cada agência
def saldo_por_agencia(agencias, saldos):
    agencias_unicas = []
    saldo_total_por_agencia = []

    for indice, agencia in enumerate(agencias):
        if agencia in agencias_unicas:
            pos = agencias_unicas.index(agencia)
            saldo_total_por_agencia[pos] += saldos[indice]
        else:
            agencias_unicas.append(agencia)
            saldo_total_por_agencia.append(saldos[indice])

    print("\n========== SALDO POR AGÊNCIA ==========")
    for n in range(len(agencias_unicas)):
        print(f"Agência: {agencias_unicas[n]} | Saldo total: R$ {saldo_total_por_agencia[n]:.2f}")


# Lista todas as contas do banco, com agência e saldo. Isso cobre, ao mesmo tempo, as funções de listar agências e contas Obs: não mostra os titulares das contas
def listar_contas(contas, agencias, saldos):
    print("\n========== LISTA DE CONTAS ==========")
    for i in range(len(contas)):
        print(f"Conta: {contas[i]} | Agência: {agencias[i]} | Saldo: R$ {saldos[i]:.2f}")