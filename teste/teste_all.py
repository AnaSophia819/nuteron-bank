from procurar_cliente import cliente_existe
from procurar_cliente import buscar_indice
from cliente import cadastrar

contas = [{"cpf": "123", "nome" : "Sophia"}]

def test_cliente_existe_true():
    assert cliente_existe(contas, "123") == True

def buscar_indice():
    assert buscar_indice(contas, "123")["nome"] == "sophia"