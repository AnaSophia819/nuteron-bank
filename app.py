from flask import Flask, request, render_template, url_for, redirect
from json_comandos import carregar_lista, salvar_lista
from conta import buscar_indice_conta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome', "")
        cpf = request.form.get('cpf', "")
        conta = request.form.get('conta', "")
        agencia = request.form.get('agencia', "")
        tipo = request.form.get('tipo', "")
        saldo = request.form.get('saldo', "")

        try:
            saldo_float = float(saldo)
        except ValueError:
            saldo_float = 0.0

        # Cria o dicionário do novo cliente
        novo_cliente = {
            'Nome': nome,
            'Cpf': cpf,
            'Saldo': saldo_float,
            'Conta': conta,
            'Agencia': agencia,
            'Tipo': tipo
        }

        clientes = carregar_lista("contas.json")
        # Verifica se a conta já existe nesta agência
        for cliente in clientes:
            if cliente.get("Conta") == conta and cliente.get("Agencia") == agencia:
                return render_template("cadastrar.html", mensagem="Já existe uma conta com esse número nesta agência.",nome=nome, cpf=cpf, conta=conta, agencia=agencia, tipo=tipo, saldo=saldo,), 400
            
        clientes.append(novo_cliente)
        salvar_lista("contas.json", clientes)

        return redirect(url_for("index"))

    return render_template("cadastrar.html")

@app.route('/depositar', methods=['GET', 'POST'])
def depositar():
    if request.method == 'POST':
        contas = carregar_lista("contas.json")

        conta_procurada =  request.form.get('conta_procurada', "")

        # Faz de acordo com o índice da função anterior 
        indice = buscar_indice_conta(conta_procurada, contas)
        
        # Se o índice (numero da conta) existir, o depoósito pode ser realizado
        if indice != None:
            valor = request.form.get('valor', "")
            if  contas[indice].get("Tipo") != "Salario":
                valor_float = float(valor)
                
                contas[indice]["Saldo"] = contas[indice].get("Saldo") + valor_float
                # Salva o novo saldo na lista "contas"
                salvar_lista("contas.json", contas)

                return redirect(url_for("index"))
            
            else: 
                return render_template("depositar.html", mensagem="Está conta não permte deposito", conta_procurada=conta_procurada, valor=valor,), 400
        
        else:
            return render_template("index.html", mensagem="Conta não encontrada",), 400

    return render_template("depositar.html")

@app.route('/sacar', methods=['GET', 'POST'])
def sacar():
    if request.method == 'POST':
        contas = carregar_lista("contas.json")

        conta_procurada = request.form.get("conta_procurada", "")
        # Faz de acordo com o índice da função anterior
        indice = buscar_indice_conta(conta_procurada, contas)
        
        # Se o índice (numero da conta) existir, o saque pode ser realizado
        if indice != None:
            valor = request.form.get("valor", "")
            if contas[indice].get("Tipo") != "poupanca": 
                valor_float = float(valor)

                # Saque só acontece se o saldo for suficiente
                if contas[indice].get("Saldo") >= valor_float:
                    contas[indice]["Saldo"] = contas[indice].get("Saldo") - valor_float
                    
                    # Salva o novo saldo na lista "saldos"
                    salvar_lista("contas.json",contas)
                    return redirect(url_for("index"))
                else:
                    return render_template("sacar.html", mensagem="Saldo insuficiente. Informe um valor menor.", conta_procurada=conta_procurada, valor=valor,), 400
            else:
                return render_template("sacar.html", mensagem="Está conta não permite saque", conta_procurada=conta_procurada, valor=valor,), 400
        else:
                return render_template("index.html", mensagem="Conta não encontrada",), 400
        
    return render_template("sacar.html")

@app.route("/relatorios")
def relatorios():
    contas = carregar_lista("contas.json")

    linhas = []
    for conta in contas:
        linhas.append({
            "numero": conta.get("Numero da conta", conta.get("Conta", "")),
            "nome": conta.get("Nome", ""),
            "cpf": conta.get("CPF", conta.get("Cpf", "")),
            "agencia": conta.get("Agencia", ""),
            "tipo": conta.get("Tipo", ""),
            "saldo": float(conta.get("Saldo", 0) or 0),
        })

    total_saldo = sum(conta["saldo"] for conta in linhas)
    quantidade_clientes = len({
        conta["cpf"] for conta in linhas if conta["cpf"]
    })
    quantidade_agencias = len({
        conta["agencia"] for conta in linhas if conta["agencia"]
    })

    contas_com_titulares = []

    for conta in contas:
        titulares = conta.get("Titulares extras", [])
        if not titulares:
            continue

        cpfs = []
        cpf_principal = conta.get("CPF", conta.get("Cpf", ""))
        if cpf_principal:
            cpfs.append(str(cpf_principal))

        cpfs.extend(
            str(titular.get("Cpf", titular.get("cpf", "")))
            for titular in titulares
            if titular.get("Cpf", titular.get("cpf", ""))
        )

        contas_com_titulares.append({
            "numero": conta.get("Numero da conta", conta.get("Conta", "")),
            "agencia": conta.get("Agencia", ""),
            "saldo": float(conta.get("Saldo", 0) or 0),
            "quantidade_titulares": 1 + len(titulares),
            "cpfs": ", ".join(cpfs),
        })

    return render_template(
        "relatorios.html",
        contas=linhas,
        contas_com_titulares=contas_com_titulares,
        total_saldo=total_saldo,
        quantidade_contas=len(linhas),
        quantidade_clientes=quantidade_clientes,
        quantidade_agencias=quantidade_agencias,
        maior_saldo=max(conta["saldo"] for conta in linhas if conta["saldo"]),
        menor_saldo=min(conta["saldo"] for conta in linhas if conta["saldo"]),
        saldo_medio=total_saldo/len(linhas)
    )

@app.route('/titular_extra', methods=['GET', 'POST'])
def titular_extra():
    if request.method == 'POST':
        contas = carregar_lista("contas.json")
        conta_procurada = request.form.get("conta_procurada", "")
        indice = buscar_indice_conta(conta_procurada, contas)
        nome_extra = request.form.get("titular_extra", "")
        cpf_extra = request.form.get("cpf_extra", "")

        if indice != None:
            contas[indice].setdefault("Titulares extras", [])
            contas[indice]["Titulares extras"].append({"Nome": nome_extra, "Cpf": cpf_extra})
            salvar_lista("contas.json", contas)
            return redirect(url_for("index"))
        else:
            return render_template("index.html", mensagem="Conta não encontrada"), 400

    return render_template("titular_extra.html")

# Executando servidor
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)