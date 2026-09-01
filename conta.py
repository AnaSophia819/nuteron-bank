def adicionar_saldo():
 deposito = input("qual o deposito? ")
saldo = saldo + deposito
print (f"foi adicionado {deposito}, o saldo agora é de {saldo}")

def mostrar_saldo():
  print = (f"o saldo é de {saldo}")

def Login():
 user = input("Digite seu CPF")
 if user not in conta:
  print ("cpf nao encontrado")
 return
nome = conta[user]["nome"] ##tem que fazer a conta antes pra definir o usuario acho q a gnt pode usar 000 000 000 01 pra testar
senha = input(f"por favor {nome} digite sua senha")
if senha == conta[user] ["senha"]:
 print (f"login realizado com sucesso, Bem vindo {nome}")
else:
  print ("senha incorreta, sera blockeado apos 3 tentativas incorretas")