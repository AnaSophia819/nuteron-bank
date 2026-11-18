from flask import Flask, request, render_template, url_for, redirect
from json_comandos import carregar_lista, salvar_lista
from conta import Conta, buscar_conta
from conta import ContaSalario, ContaPoupanca, ContaCorrente

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome', "")
        cpf = request.form.get('cpf', "")
        numero_conta = request.form.get('conta', "")
        agencia = request.form.get('agencia', "")
        tipo = request.form.get('tipo', "")
        saldo = request.form.get('saldo', "")

        try:
            saldo_float = float(saldo)
        except ValueError:
            saldo_float = 0.0

        dados_json = carregar_lista("contas.json")
        contas_obj = [Conta.from_dict(d) for d in dados_json]

        # Verifica se a conta já existe nesta agência
        for c in contas_obj:
            if c.numero == numero_conta and c.agencia == agencia:
                return render_template("cadastrar.html", mensagem="Já existe uma conta com esse número nesta agência.", nome=nome, cpf=cpf, conta=numero_conta, agencia=agencia, tipo=tipo, saldo=saldo), 400

        tipo_normalizado = tipo.strip().casefold()

        if tipo_normalizado == "salário" or tipo_normalizado == "salario":
            nova_conta = ContaSalario(numero_conta, agencia, saldo_float, cpf, nome)
        elif tipo_normalizado == "poupança" or tipo_normalizado == "poupanca":
            nova_conta = ContaPoupanca(numero_conta, agencia, saldo_float, cpf, nome)
        elif tipo_normalizado == "corrente":
            nova_conta = ContaCorrente(numero_conta, agencia, saldo_float, cpf, nome)
        else:
            return render_template(
                "cadastrar.html",
                mensagem="Tipo inválido. Use Corrente, Poupança ou Salário."
            ), 400
        
        contas_obj.append(nova_conta)
        salvar_lista("contas.json", [c.to_dict() for c in contas_obj])
        return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.route('/depositar', methods=['GET', 'POST'])
def depositar():
    if request.method == 'POST':
        dados_json = carregar_lista("contas.json")
        contas_obj = [Conta.from_dict(d) for d in dados_json]

        conta_procurada = request.form.get('conta_procurada', "")
        valor = request.form.get('valor', "")

        conta_alvo = buscar_conta(conta_procurada, contas_obj)
        
        if conta_alvo:
            sucesso, msg = conta_alvo.depositar(valor)
            if sucesso:
                salvar_lista("contas.json", [c.to_dict() for c in contas_obj])
                return redirect(url_for("index"))
            else:
                return render_template("depositar.html", mensagem=msg, conta_procurada=conta_procurada, valor=valor), 400
        else:
            return render_template("index.html", mensagem="Conta não encontrada"), 400

    return render_template("depositar.html")


@app.route('/sacar', methods=['GET', 'POST'])
def sacar():
    if request.method == 'POST':
        dados_json = carregar_lista("contas.json")
        contas_obj = [Conta.from_dict(d) for d in dados_json]

        conta_procurada = request.form.get("conta_procurada", "")
        valor = request.form.get("valor", "")
        
        conta_alvo = buscar_conta(conta_procurada, contas_obj)
        
        if conta_alvo:
            sucesso, msg = conta_alvo.sacar(valor)
            if sucesso:
                salvar_lista("contas.json", [c.to_dict() for c in contas_obj])
                return redirect(url_for("index"))
            else:
                return render_template("sacar.html", mensagem=msg, conta_procurada=conta_procurada, valor=valor), 400
        else:
            return render_template("index.html", mensagem="Conta não encontrada"), 400
            
    return render_template("sacar.html")


@app.route('/saldo', methods=['GET', 'POST'])
def consultar_saldo():
    if request.method == 'POST':
        dados_json = carregar_lista("contas.json")
        contas_obj = [Conta.from_dict(d) for d in dados_json]
        
        conta_procurada = request.form.get("conta_procurada", "")
        conta_alvo = buscar_conta(conta_procurada, contas_obj)
        
        if conta_alvo:
            return render_template("saldo.html", saldo=conta_alvo.saldo, conta_procurada=conta_procurada)
        else:
            return render_template("saldo.html", mensagem="Conta não encontrada.")
            
    return render_template("saldo.html")


@app.route('/titular_extra', methods=['GET', 'POST'])
def titular_extra():
    if request.method == 'POST':
        dados_json = carregar_lista("contas.json")
        contas_obj = [Conta.from_dict(d) for d in dados_json]
        
        conta_procurada = request.form.get("conta_procurada", "")
        nome_extra = request.form.get("titular_extra", "")
        cpf_extra = request.form.get("cpf_extra", "")

        conta_alvo = buscar_conta(conta_procurada, contas_obj)

        if conta_alvo:
            conta_alvo.adicionar_titular(nome_extra, cpf_extra)
            salvar_lista("contas.json", [c.to_dict() for c in contas_obj])
            return redirect(url_for("index"))
        else:
            return render_template("index.html", mensagem="Conta não encontrada"), 400

    return render_template("titular_extra.html")


@app.route("/relatorios")
def relatorios():
    dados_json = carregar_lista("contas.json")
    contas_obj = [Conta.from_dict(d) for d in dados_json]

    if not contas_obj:
        return render_template(
            "relatorios.html",
            contas=[],
            contas_com_titulares=[],
            total_saldo=0.0,
            quantidade_contas=0,
            quantidade_clientes=0,
            quantidade_agencias=0,
            maior_saldo=0.0,
            menor_saldo=0.0,
            saldo_medio=0.0
        )

    total_saldo = sum(c.saldo for c in contas_obj)
    quantidade_clientes = len({c.cpf for c in contas_obj if c.cpf})
    quantidade_agencias = len({c.agencia for c in contas_obj if c.agencia})
    maior_saldo = max(c.saldo for c in contas_obj)
    menor_saldo = min(c.saldo for c in contas_obj)
    saldo_medio = total_saldo / len(contas_obj)

    contas_com_titulares = []
    for c in contas_obj:
        if not c.titulares_extras:
            continue
            
        cpfs = [str(c.cpf)] if c.cpf else []
        cpfs.extend(str(t.get("Cpf", t.get("cpf", ""))) for t in c.titulares_extras if t.get("Cpf", t.get("cpf", "")))
        
        contas_com_titulares.append({
            "numero": c.numero,
            "agencia": c.agencia,
            "saldo": c.saldo,
            "quantidade_titulares": 1 + len(c.titulares_extras),
            "cpfs": ", ".join(cpfs),
        })

    return render_template(
        "relatorios.html",
        contas=contas_obj,
        contas_com_titulares=contas_com_titulares,
        total_saldo=total_saldo,
        quantidade_contas=len(contas_obj),
        quantidade_clientes=quantidade_clientes,
        quantidade_agencias=quantidade_agencias,
        maior_saldo=maior_saldo,
        menor_saldo=menor_saldo,
        saldo_medio=saldo_medio
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)