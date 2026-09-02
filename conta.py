def abrir_conta():
    
    saldo_atual = 0.0
    print(f"Conta aberta! Saldo inicial: {saldo_atual}")
    return saldo_atual

def adicionar_saldo(saldo_atual):

  deposito = float(input("Informe o valor do depósito:"))

  if deposito > 0:
    saldo_atual += deposito
    return saldo_atual
  else: 
     print("Valor inválido")

  return saldo_atual

def mostrar_saldo(saldo_atual):

  print (f"o saldo é de {saldo_atual}")

def realizar_saque(saldo_atual):

  saque = float(input("Informe o valor do saque:"))

  if saque > 0:
    if saque >= saldo_atual:
      print("Saldo insuficiente")
    else:
      saldo_atual -= saque
      print(f"Saque realizado no valor de {saque}")
      return saldo_atual
  else:
    print("Valor inválido")

  return saldo_atual