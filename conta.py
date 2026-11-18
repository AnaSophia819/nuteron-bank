from abc import ABC, abstractmethod
from json_comandos import salvar_lista # Importar do arquivo de comandos do json a função "salvar_lista" 
from cliente import Cliente # Importar do arquivo "cliente" a classe "Cliente"

class Conta(ABC):
    def __init__(self, numero, agencia, saldo, cpf, nome, tipo):
        self.numero = numero
        self.agencia = agencia
        self.saldo = float(saldo)
        self.cliente = Cliente(nome, cpf) 
        self.tipo = tipo
        self.titulares_extras = []

    @property
    def cpf(self):
        return self.cliente.cpf

    @property
    def nome(self):
        return self.cliente.nome


    @abstractmethod
    def depositar(self, valor):
        pass

    @abstractmethod
    def sacar(self, valor):
        pass

        
    # --- INTEGRAÇÃO COM JSON ---
    def to_dict(self):
        """Converte o objeto Conta para um dicionário (para salvar no JSON)"""
        return {
            "Conta": self.numero,
            "Agencia": self.agencia,
            "Saldo": self.saldo,
            "CPF": self.cliente.cpf,
            "Nome": self.cliente.nome,
            "Tipo": self.tipo,
        }
    
    @classmethod
    def from_dict(cls, dados):
        """Cria um objeto Conta a partir de um dicionário (vindo do JSON)"""
        tipo = str(dados.get("Tipo", "")).strip().casefold()

        classes = {
            "corrente": ContaCorrente,
            "salário": ContaSalario,
            "salario": ContaSalario,
            "poupança": ContaPoupanca,
            "poupanca": ContaPoupanca,
        }

        if tipo not in classes:
            raise ValueError(f"Tipo de conta inválido no JSON: {tipo!r}")

        classe_conta = classes[tipo]
        return classe_conta(
            numero=dados.get("Conta", dados.get("Numero da conta", "")),
            agencia=dados.get("Agencia", ""),
            saldo=dados.get("Saldo", 0.0),
            cpf=dados.get("CPF", dados.get("Cpf", "")),
            nome=dados.get("Nome", ""),
        )

def buscar_conta(numero_procurado, lista_contas_obj):
    """Busca e retorna o objeto Conta que corresponde ao número"""
    for conta in lista_contas_obj:
        if conta.numero == numero_procurado:
            return conta
    return None

class ContaSalario(Conta):
    def __init__(self, numero, agencia, saldo, cpf, nome):
        super().__init__(numero, agencia, saldo, cpf, nome, tipo="Salário")  # Inicializa a lista de titulares extras como vazia

    def depositar(self, valor):
        return False, "Essa conta não aceita depósito"

    def sacar(self, valor):
        valor = float(valor)

        if self.saldo < valor:
            return False, "Saldo insuficiente. Informe um valor menor"
        else:
            self.saldo -= valor
            return True, "Saque realizado com sucesso."

class ContaPoupanca(Conta):
    def __init__(self, numero, agencia, saldo, cpf, nome):
        super().__init__(numero, agencia, saldo, cpf, nome, tipo="poupança") 
        self.rendimento = 0.01 # Inicializa a lista de titulares extras como vazia

    def depositar(self, valor):
        valor = float(valor)
        self.saldo += valor
        return True, "Depósito realizado com sucesso"

    def sacar(self, valor):
        valor = float(valor)
        
        if self.saldo < valor:
            return False, "Saldo insuficiente. Informe um valor menor"
        else:
            self.saldo -= float(valor)
            return True, "Saque realizado com sucesso."

    def calcular_rendimento(self):
        """Calcula o rendimento da conta poupança"""
        rendimento = self.saldo * self.rendimento
        self.saldo += rendimento
        return rendimento
    
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, saldo, cpf, nome):
        super().__init__(numero, agencia, saldo, cpf, nome, tipo="corrente")

    def depositar(self, valor):
        valor = float(valor)
        self.saldo += valor
        return True, "Depósito realizado com sucesso."

    def sacar(self, valor):
        valor = float(valor)

        if valor > self.saldo:
            return False, "Saldo insuficiente."

        self.saldo -= valor
        return True, "Saque realizado com sucesso."