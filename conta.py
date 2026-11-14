from json_comandos import salvar_lista # Importar do arquivo de comandos do json a função "salvar_lista"
from cliente import cadastrar # Importar do arquivo "cliente" a função "cadastrar"

class Conta:
    def __init__(self, numero, agencia, saldo, cpf, nome, tipo, titulares_extras=None):
        self.numero = numero
        self.agencia = agencia
        self.saldo = float(saldo)
        self.cpf = cpf
        self.nome = nome
        self.tipo = tipo
        self.titulares_extras = titulares_extras if titulares_extras is not None else []

    def depositar(self, valor):
        if self.tipo.lower() == "salario" or self.tipo.lower() == "salário":
            return False, "Essa conta não aceita deposito"

        self.saldo += float(valor)
        return True, "Depósito realizado com sucesso"

    def sacar(self, valor):

        if self.tipo.lower() == "poupanca" or self.tipo.lower() == "poupança":
            return False, "Essa conta não permite saque."
        elif self.saldo < float(valor):
            return False, "Saldo insuficiente. Informe um valor menor"
        else:
            self.saldo -= float(valor)
            return True, "Saque realizado com sucesso."

    # Função para fazer conta conjunta
    def adicionar_titular_extra(self, nome, cpf):
        self.titulares_extras.append({"Nome":nome, "Cpf": cpf})
        
    # --- INTEGRAÇÃO COM JSON ---
    def to_dict(self):
        """Converte o objeto Conta para um dicionário (para salvar no JSON)"""
        return {
            "Conta": self.numero,
            "Agencia": self.agencia,
            "Saldo": self.saldo,
            "CPF": self.cpf,
            "Nome": self.nome,
            "Tipo": self.tipo,
            "Titulares extras": self.titulares_extras
        }
    
    @classmethod
    def from_dict(cls, dados):
        """Cria um objeto Conta a partir de um dicionário (vindo do JSON)"""
        return cls(
            numero=dados.get("Conta", dados.get("Numero da conta", "")),
            agencia=dados.get("Agencia", ""),
            saldo=dados.get("Saldo", 0.0),
            cpf=dados.get("CPF", dados.get("Cpf", "")),
            nome=dados.get("Nome", ""),
            tipo=dados.get("Tipo", ""),
            titulares_extras=dados.get("Titulares extras", [])
        )

def buscar_conta(numero_procurado, lista_contas_obj):
    """Busca e retorna o objeto Conta que corresponde ao número"""
    for conta in lista_contas_obj:
        if conta.numero == numero_procurado:
            return conta
    return None
