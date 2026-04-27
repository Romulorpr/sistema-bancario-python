# conta.py — Classe que representa uma conta bancária e suas regras de negócio

LIMITE_SAQUE = 500   # Valor máximo permitido por saque
MAX_SAQUES   = 3     # Número máximo de saques permitidos por sessão


class Conta:
    def __init__(self, id, nome, cpf, saldo=0.0, saques=0):
        self.id     = id
        self.nome   = nome
        self.cpf    = cpf
        self.saldo  = saldo
        self.saques = saques  # Contador de saques realizados na sessão

    def depositar(self, valor):
        if valor <= 0:
            return False, "Valor inválido."
        self.saldo += valor
        return True, f"Depósito de R$ {valor:.2f} realizado com sucesso."

    def sacar(self, valor):
        if valor <= 0:
            return False, "Valor inválido."
        if valor > self.saldo:
            return False, "Saldo insuficiente."
        if valor > LIMITE_SAQUE:
            return False, f"Valor excede o limite por saque (R$ {LIMITE_SAQUE:.2f})."
        if self.saques >= MAX_SAQUES:
            return False, "Limite de saques diários atingido."

        self.saldo  -= valor
        self.saques += 1
        return True, f"Saque de R$ {valor:.2f} realizado com sucesso."

    def __repr__(self):
        return f"Conta(id={self.id}, nome={self.nome}, cpf={self.cpf}, saldo={self.saldo:.2f})"
