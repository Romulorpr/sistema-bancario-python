# banco.py — Acesso ao banco de dados SQLite (CRUD de contas e transações)

import sqlite3

DB_PATH = "dados.db"  # Arquivo gerado automaticamente na primeira execução


def conectar():
    return sqlite3.connect(DB_PATH)  # Cria o arquivo se não existir


def criar_tabelas():
    """Cria as tabelas no banco caso ainda não existam."""
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS contas (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                nome   TEXT    NOT NULL,
                cpf    TEXT    NOT NULL UNIQUE,
                saldo  REAL    DEFAULT 0.0,
                saques INTEGER DEFAULT 0
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER NOT NULL,
                tipo     TEXT    NOT NULL,  -- 'deposito' ou 'saque'
                valor    REAL    NOT NULL,
                data     TEXT    DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (conta_id) REFERENCES contas(id)
            )
        """)


# ── CRUD de contas ────────────────────────────────────────────────

def criar_conta(nome, cpf):
    """Cadastra uma nova conta. Retorna (True, id) ou (False, mensagem)."""
    try:
        with conectar() as con:
            cur = con.execute(
                "INSERT INTO contas (nome, cpf) VALUES (?, ?)", (nome, cpf)
            )
            return True, cur.lastrowid
    except sqlite3.IntegrityError:
        return False, "CPF já cadastrado."


def buscar_conta(cpf):
    """Busca conta pelo CPF. Retorna um objeto Conta ou None."""
    from conta import Conta
    with conectar() as con:
        row = con.execute(
            "SELECT id, nome, cpf, saldo, saques FROM contas WHERE cpf = ?", (cpf,)
        ).fetchone()
    return Conta(*row) if row else None


def listar_contas():
    """Retorna todas as contas cadastradas como lista de objetos Conta."""
    from conta import Conta
    with conectar() as con:
        rows = con.execute(
            "SELECT id, nome, cpf, saldo, saques FROM contas"
        ).fetchall()
    return [Conta(*row) for row in rows]


def atualizar_conta(conta):
    """Salva saldo e número de saques da conta no banco."""
    with conectar() as con:
        con.execute(
            "UPDATE contas SET saldo = ?, saques = ? WHERE id = ?",
            (conta.saldo, conta.saques, conta.id)
        )


def atualizar_nome(cpf, novo_nome):
    """Atualiza o nome do titular da conta."""
    with conectar() as con:
        con.execute(
            "UPDATE contas SET nome = ? WHERE cpf = ?", (novo_nome, cpf)
        )


def excluir_conta(cpf):
    """Remove a conta e todas as suas transações do banco."""
    with conectar() as con:
        row = con.execute(
            "SELECT id FROM contas WHERE cpf = ?", (cpf,)
        ).fetchone()
        if not row:
            return False, "Conta não encontrada."
        conta_id = row[0]
        con.execute("DELETE FROM transacoes WHERE conta_id = ?", (conta_id,))
        con.execute("DELETE FROM contas WHERE id = ?", (conta_id,))
    return True, "Conta encerrada com sucesso."


# ── Transações ────────────────────────────────────────────────────

def registrar_transacao(conta_id, tipo, valor):
    """Registra uma transação (depósito ou saque) para a conta."""
    with conectar() as con:
        con.execute(
            "INSERT INTO transacoes (conta_id, tipo, valor) VALUES (?, ?, ?)",
            (conta_id, tipo, valor)
        )


def extrato(conta_id):
    """Retorna a lista de transações da conta em ordem cronológica."""
    with conectar() as con:
        rows = con.execute(
            "SELECT tipo, valor, data FROM transacoes WHERE conta_id = ? ORDER BY id",
            (conta_id,)
        ).fetchall()
    return rows  # lista de tuplas (tipo, valor, data)
