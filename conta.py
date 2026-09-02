def adicionar_saldo(saldo_atual):
  deposito = float(input("Informe o valor do depósito:"))
  if deposito > 0:
    saldo_atual += deposito
    return saldo_atual
  else: 
     print("Valor inválido")

def mostrar_saldo(saldo):
  return (f"o saldo é de {saldo}")

def abrir_conta():
    saldo = 0.0
    return saldo

def realizar_saque(saldo_atual):
  saque = float(input("Informe o valor do saque:"))

  if saque > 0:
    if saque <= saldo_atual:
      print("Saldo insuficiente")
    else:
      saldo_atual -= saque
      return saldo_atual
  else:
    print("Valor inválido")