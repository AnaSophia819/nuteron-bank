import json

# Comando geral em json para salvar as listas que serão feitas durante o código
def salvar_lista(nome_arquivo, lista):
    with open(nome_arquivo, "w") as arquivo:
        json.dump(lista, arquivo)

# Comando geral em json para carregar as listas durante o código
def carregar_lista(nome_arquivo):

    try:
        with open(nome_arquivo, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    