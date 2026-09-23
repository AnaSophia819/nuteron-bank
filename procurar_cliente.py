# Função para procurar na lista dos cpfs se o cliente digitado existe
def cliente_existe(cpf_digitado, cpfs):

    if cpf_digitado in cpfs:
        print("CPF já cadastrado.")
        return True
    else: 
        return False