import json

def salvar_lista(nome_arquivo, lista):
    with open(nome_arquivo, "w") as arquivo:
        json.dump(lista, arquivo)

def carregar_lista(nome_arquivo):

    try:
        with open(nome_arquivo, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    