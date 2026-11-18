from copy import deepcopy

import pytest

import app as bank_app


@pytest.fixture
def client():
    bank_app.app.config.update(TESTING=True)
    return bank_app.app.test_client()


@pytest.fixture
def account_store(monkeypatch):
    accounts = [
        {
            "Nome": "Ana",
            "Cpf": "111",
            "Saldo": 100.0,
            "Conta": "123",
            "Agencia": "0001",
            "Tipo": "Corrente",
        }
    ]
    saved_lists = []
    monkeypatch.setattr(bank_app, "carregar_lista", lambda filename: accounts)
    monkeypatch.setattr(
        bank_app,
        "salvar_lista",
        lambda filename, data: saved_lists.append((filename, deepcopy(data))),
    )
    return accounts, saved_lists


@pytest.mark.parametrize(
    "path",
    ["/", "/cadastrar", "/depositar", "/sacar", "/titular_extra"],
)
def test_pages_render(client, path):
    response = client.get(path)

    assert response.status_code == 200


def test_cadastrar_creates_account_and_redirects(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/cadastrar",
        data={
            "nome": "Bruna",
            "cpf": "222",
            "saldo": "250.50",
            "conta": "456",
            "agencia": "0002",
            "tipo": "Poupança",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    assert saved_lists == [
        (
            "contas.json",
            [
                {
                    "Nome": "Ana",
                    "Cpf": "111",
                    "Saldo": 100.0,
                    "Conta": "123",
                    "Agencia": "0001",
                    "Tipo": "Corrente",
                },
                {
                    "Nome": "Bruna",
                    "Cpf": "222",
                    "Saldo": 250.5,
                    "Conta": "456",
                    "Agencia": "0002",
                    "Tipo": "Poupança",
                },
            ],
        )
    ]


def test_cadastrar_uses_zero_for_invalid_balance(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/cadastrar",
        data={
            "nome": "Bruna",
            "cpf": "222",
            "saldo": "inválido",
            "conta": "456",
            "agencia": "0002",
            "tipo": "Corrente",
        },
    )

    assert response.status_code == 302
    assert saved_lists[0][1][-1]["Saldo"] == 0.0


def test_cadastrar_rejects_duplicate_account_in_same_agency(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/cadastrar",
        data={
            "nome": "Outra pessoa",
            "cpf": "222",
            "saldo": "10",
            "conta": "123",
            "agencia": "0001",
            "tipo": "Corrente",
        },
    )

    assert response.status_code == 400
    assert "Já existe uma conta" in response.get_data(as_text=True)
    assert saved_lists == []


def test_depositar_updates_balance_and_redirects(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/depositar", data={"conta_procurada": "123", "valor": "25.50"}
    )

    assert response.status_code == 302
    assert saved_lists[0][1][0]["Saldo"] == 125.5


def test_depositar_rejects_salary_account(client, account_store):
    accounts, saved_lists = account_store
    accounts[0]["Tipo"] = "Salario"

    response = client.post(
        "/depositar", data={"conta_procurada": "123", "valor": "25"}
    )

    assert response.status_code == 400
    assert "não permte deposito" in response.get_data(as_text=True)
    assert saved_lists == []


def test_depositar_reports_missing_account(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/depositar", data={"conta_procurada": "999", "valor": "25"}
    )

    assert response.status_code == 400
    assert "Conta não encontrada" in response.get_data(as_text=True)
    assert saved_lists == []


def test_sacar_updates_balance_and_redirects(client, account_store):
    _, saved_lists = account_store

    response = client.post("/sacar", data={"conta_procurada": "123", "valor": "40"})

    assert response.status_code == 302
    assert saved_lists[0][1][0]["Saldo"] == 60.0


def test_sacar_rejects_withdrawal_above_balance(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/sacar", data={"conta_procurada": "123", "valor": "101"}
    )

    assert response.status_code == 400
    assert "Saldo insuficiente" in response.get_data(as_text=True)
    assert saved_lists == []


def test_sacar_rejects_savings_account(client, account_store):
    accounts, saved_lists = account_store
    accounts[0]["Tipo"] = "poupanca"

    response = client.post("/sacar", data={"conta_procurada": "123", "valor": "10"})

    assert response.status_code == 400
    assert "não permite saque" in response.get_data(as_text=True)
    assert saved_lists == []


def test_sacar_reports_missing_account(client, account_store):
    _, saved_lists = account_store

    response = client.post("/sacar", data={"conta_procurada": "999", "valor": "10"})

    assert response.status_code == 400
    assert "Conta não encontrada" in response.get_data(as_text=True)
    assert saved_lists == []


def test_relatorios_renders_account_totals(client, monkeypatch):
    accounts = [
        {
            "Nome": "Ana",
            "CPF": "111",
            "Saldo": 100,
            "Numero da conta": "123",
            "Agencia": "0001",
            "Tipo": "Corrente",
            "Titulares extras": [{"Nome": "Bruna", "Cpf": "222"}],
        },
        {
            "Nome": "Ana",
            "CPF": "111",
            "Saldo": 200,
            "Conta": "456",
            "Agencia": "0002",
            "Tipo": "Poupança",
        },
    ]
    monkeypatch.setattr(bank_app, "carregar_lista", lambda filename: accounts)

    response = client.get("/relatorios")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "<span>Contas</span><strong>2</strong>" in html
    assert "<span>Clientes</span><strong>1</strong>" in html
    assert "<span>Agências</span><strong>2</strong>" in html
    assert "<strong>R$ 300.00</strong>" in html
    assert "<strong>R$ 150.00</strong>" in html
    assert "123" in html
    assert "456" in html
    assert "Contas com titulares extras" in html
    assert "Quantidade de titulares" in html
    assert "111, 222" in html


def test_titular_extra_appends_holder_and_redirects(client, account_store):
    _, saved_lists = account_store

    response = client.post(
        "/titular_extra",
        data={
            "conta_procurada": "123",
            "titular_extra": "Bruna",
            "cpf_extra": "222",
        },
    )

    assert response.status_code == 302
    assert saved_lists[0][1][0]["Titulares extras"] == [
        {"Nome": "Bruna", "Cpf": "222"}
    ]
