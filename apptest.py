import math
from pathlib import Path

from flask import Flask, abort, render_template, request, url_for

from json_comandos import carregar_lista, salvar_lista

app = Flask(__name__)
app.config["DATA_FILE"] = str(Path(app.root_path) / "contas.json")

REPORTS = {
    "contas-por-cpf": "Contas por CPF",
    "contas-por-agencia": "Contas por agência",
    "contas-multiplos-titulares": "Contas com mais de um titular",
    "saldo-por-cliente": "Saldo por cliente",
    "saldo-por-agencia": "Saldo total por agência",
    "clientes": "Lista de clientes",
    "contas": "Lista de contas",
    "geral": "Relatório geral",
}

ACCOUNT_TYPES = {"corrente", "salario", "poupanca"}


def load_accounts():
    accounts = carregar_lista(app.config["DATA_FILE"])
    if not isinstance(accounts, list) or any(not isinstance(item, dict) for item in accounts):
        raise ValueError("O arquivo de contas precisa conter uma lista de contas válida.")
    return accounts


def save_accounts(accounts):
    salvar_lista(app.config["DATA_FILE"], accounts)


def clean_field(name):
    return request.form.get(name, "").strip()


def parse_amount(value, field_name, allow_zero=False):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Informe um valor numérico válido para {field_name}.") from None

    if not math.isfinite(amount) or amount < 0 or (amount == 0 and not allow_zero):
        if allow_zero:
            raise ValueError(f"{field_name} precisa ser um valor finito maior ou igual a zero.")
        raise ValueError(f"{field_name} precisa ser um valor finito maior que zero.")
    return amount


def render_message(message, is_error=False, status=200):
    return (
        render_template(
            "result.html",
            title="Operação bancária",
            message=message,
            is_error=is_error,
            home_url=url_for("index"),
        ),
        status,
    )


def unique_clients(accounts):
    clients = {}
    for account in accounts:
        cpf = account.get("CPF")
        if cpf:
            clients.setdefault(cpf, account.get("Nome", ""))
        for holder in account.get("Titulares extras", []):
            holder_cpf = holder.get("cpf")
            if holder_cpf:
                clients.setdefault(holder_cpf, holder.get("Nome", ""))
    return clients


def report_data(report_name, accounts):
    if report_name not in REPORTS:
        abort(404)

    if report_name == "contas-por-cpf":
        counts = {}
        for account in accounts:
            cpf = account.get("CPF", "")
            counts[cpf] = counts.get(cpf, 0) + 1
        return ["CPF", "Quantidade de contas"], [[cpf, count] for cpf, count in counts.items()]

    if report_name == "contas-por-agencia":
        counts = {}
        for account in accounts:
            agency = account.get("Agencia", "")
            counts[agency] = counts.get(agency, 0) + 1
        return ["Agência", "Quantidade de contas"], [[agency, count] for agency, count in counts.items()]

    if report_name == "contas-multiplos-titulares":
        rows = []
        for account in accounts:
            extra_holders = account.get("Titulares extras", [])
            rows.append(
                [
                    account.get("Numero da conta", ""),
                    account.get("Agencia", ""),
                    1 + len(extra_holders),
                    ", ".join(
                        [str(account.get("CPF", ""))]
                        + [str(holder.get("cpf", "")) for holder in extra_holders]
                    ),
                ]
            )
        return ["Conta", "Agência", "Quantidade de titulares", "CPFs"], rows

    if report_name == "saldo-por-cliente":
        balances = {}
        for account in accounts:
            cpf = account.get("CPF", "")
            balances[cpf] = balances.get(cpf, 0) + float(account.get("Saldo", 0))
        return ["CPF", "Saldo total (R$)"], [[cpf, f"{balance:.2f}"] for cpf, balance in balances.items()]

    if report_name == "saldo-por-agencia":
        balances = {}
        for account in accounts:
            agency = account.get("Agencia", "")
            balances[agency] = balances.get(agency, 0) + float(account.get("Saldo", 0))
        return [
            "Agência",
            "Saldo total (R$)",
        ], [[agency, f"{balance:.2f}"] for agency, balance in balances.items()]

    if report_name == "clientes":
        clients = unique_clients(accounts)
        return ["Nome", "CPF"], [[name, cpf] for cpf, name in clients.items()]

    if report_name == "contas":
        return (
            ["Conta", "Agência", "Titular", "CPF", "Tipo", "Saldo (R$)"],
            [
                [
                    account.get("Numero da conta", ""),
                    account.get("Agencia", ""),
                    account.get("Nome", ""),
                    account.get("CPF", ""),
                    account.get("Tipo", ""),
                    f"{float(account.get('Saldo', 0)):.2f}",
                ]
                for account in accounts
            ],
        )

    total_balance = sum(float(account.get("Saldo", 0)) for account in accounts)
    agencies = {account.get("Agencia") for account in accounts if account.get("Agencia")}
    summary = [
        ["Quantidade de contas", len(accounts)],
        ["Quantidade de clientes", len(unique_clients(accounts))],
        ["Saldo total (R$)", f"{total_balance:.2f}"],
        ["Quantidade de agências", len(agencies)],
    ]
    return ["Indicador", "Resultado"], summary


@app.route("/")
def index():
    return render_template("index.html", reports=REPORTS)


@app.post("/accounts")
def create_account():
    cpf = clean_field("cpf")
    name = clean_field("name")
    account_number = clean_field("account_number")
    agency = clean_field("agency")
    account_type = clean_field("account_type").lower()

    if not all((cpf, name, account_number, agency)):
        return render_message("Preencha todos os campos da conta.", True, 400)
    if account_type not in ACCOUNT_TYPES:
        return render_message("Selecione um tipo de conta válido.", True, 400)

    try:
        initial_balance = parse_amount(clean_field("initial_balance"), "Saldo inicial", allow_zero=True)
        accounts = load_accounts()
    except ValueError as error:
        return render_message(str(error), True, 400)

    if any(account.get("Numero da conta") == account_number for account in accounts):
        return render_message("Já existe uma conta com esse número.", True, 409)

    registered_client = next((account for account in accounts if account.get("CPF") == cpf), None)
    if registered_client:
        name = registered_client.get("Nome", name)

    accounts.append(
        {
            "Numero da conta": account_number,
            "Agencia": agency,
            "Saldo": initial_balance,
            "CPF": cpf,
            "Nome": name,
            "Tipo": account_type,
        }
    )
    save_accounts(accounts)
    return render_message(f"Conta {account_number} criada com sucesso.")


@app.get("/balance")
def balance():
    account_number = request.args.get("account_number", "").strip()
    if not account_number:
        return render_message("Informe o número da conta para consultar o saldo.", True, 400)

    accounts = load_accounts()
    account = next(
        (item for item in accounts if item.get("Numero da conta") == account_number),
        None,
    )
    if account is None:
        return render_message("Conta não encontrada.", True, 404)

    return render_template(
        "result.html",
        title="Saldo da conta",
        message=f"Saldo da conta {account_number}: R$ {float(account.get('Saldo', 0)):.2f}",
        is_error=False,
        home_url=url_for("index"),
    )


def change_balance(operation):
    account_number = clean_field("account_number")
    try:
        amount = parse_amount(clean_field("amount"), "Valor")
        accounts = load_accounts()
    except ValueError as error:
        return render_message(str(error), True, 400)

    account = next(
        (item for item in accounts if item.get("Numero da conta") == account_number),
        None,
    )
    if account is None:
        return render_message("Conta não encontrada.", True, 404)

    account_type = str(account.get("Tipo", "")).lower()
    normalized_type = account_type.replace("á", "a").replace("ã", "a")
    if operation == "deposit" and normalized_type in {"salario", "salário"}:
        return render_message("Esta conta não aceita depósitos.", True, 400)
    if operation == "withdraw" and normalized_type in {"poupanca", "poupança"}:
        return render_message("Esta conta não permite saques.", True, 400)

    current_balance = float(account.get("Saldo", 0))
    if not math.isfinite(current_balance) or current_balance < 0:
        return render_message("O saldo armazenado para esta conta é inválido.", True, 500)
    if operation == "withdraw" and current_balance < amount:
        return render_message("Saldo insuficiente.", True, 400)

    account["Saldo"] = current_balance + amount if operation == "deposit" else current_balance - amount
    save_accounts(accounts)
    operation_text = "Depósito" if operation == "deposit" else "Saque"
    return render_message(f"{operation_text} realizado. Novo saldo: R$ {account['Saldo']:.2f}")


@app.post("/deposit")
def deposit():
    return change_balance("deposit")


@app.post("/withdraw")
def withdraw():
    return change_balance("withdraw")


@app.post("/holders")
def add_holder():
    account_number = clean_field("account_number")
    cpf = clean_field("cpf")
    name = clean_field("name")
    if not account_number or not cpf or not name:
        return render_message("Informe conta, CPF e nome do titular.", True, 400)

    accounts = load_accounts()
    account = next(
        (item for item in accounts if item.get("Numero da conta") == account_number),
        None,
    )
    if account is None:
        return render_message("Conta não encontrada.", True, 404)

    extra_holders = account.setdefault("Titulares extras", [])
    if cpf == account.get("CPF") or any(holder.get("cpf") == cpf for holder in extra_holders):
        return render_message("Este CPF já é titular desta conta.", True, 409)

    registered_client = next((item for item in accounts if item.get("CPF") == cpf), None)
    if registered_client:
        name = registered_client.get("Nome", name)
    extra_holders.append({"Nome": name, "cpf": cpf})
    save_accounts(accounts)
    return render_message(f"Titular adicionado à conta {account_number}.")


@app.get("/reports/<report_name>")
def show_report(report_name):
    accounts = load_accounts()
    headers, rows = report_data(report_name, accounts)
    return render_template(
        "report.html",
        title=REPORTS[report_name],
        headers=headers,
        rows=rows,
        home_url=url_for("index"),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
