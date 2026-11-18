# Função para procurar na lista dos cpfs se o cliente digitado existe
def cliente_existe(contas, cpf):
    for i in contas:
        if i.get("CPF") == cpf:
            return True
    return False

def buscar_indice (contas, cpf):
    for i in contas:
        if i["CPF"] == cpf:
            return i
    return None