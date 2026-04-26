# sisbanco.py — Lógica do sistema bancário (sem interface)

saldo = 0
limite = 500        # Valor máximo permitido por saque
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3   # Número máximo de saques permitidos por sessão


def depositar(valor):
    global saldo, extrato
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return "Depósito realizado com sucesso!"
    return "Valor inválido"


def sacar(valor):
    global saldo, extrato, numero_saques

    if valor > saldo:
        return "Saldo insuficiente"
    elif valor > limite:
        return "Excede limite"
    elif numero_saques >= LIMITE_SAQUES:  # Bloqueia após atingir o limite de saques
        return "Limite de saques atingido"
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return "Saque realizado com sucesso!"
    return "Valor inválido"


def ver_extrato():
    return extrato if extrato else "Sem movimentações"


def ver_saldo():
    return saldo