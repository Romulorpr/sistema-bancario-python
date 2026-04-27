# interface.py — Interface gráfica com tkinter

import tkinter as tk
from tkinter import messagebox
import banco

conta_ativa = None  # Conta carregada na sessão atual


def campo_cpf(parent, row):
    """Cria um campo CPF com restrições nativas:
    - Aceita apenas dígitos numéricos
    - Bloqueia qualquer entrada após 11 dígitos
    - Exibe contador 0/11 que fica verde ao completar
    Retorna o widget Entry para uso externo."""

    vcmd = parent.register(lambda txt: txt == "" or (txt.isdigit() and len(txt) <= 11))
    entry = tk.Entry(
        parent,
        font=("Segoe UI", 11),
        validate="key",                # Valida a cada tecla pressionada
        validatecommand=(vcmd, "%P"), # %P = valor completo do campo após a tecla
    )
    entry.grid(row=row, column=0, columnspan=2, sticky="ew", ipady=6, pady=(2, 2))

    label_contador = tk.Label(parent, text="0/11", font=("Segoe UI", 8), fg="gray")
    label_contador.grid(row=row + 1, column=1, sticky="e", pady=(0, 8))

    def atualizar_contador(*_):
        n = len(entry.get())
        label_contador.config(text=f"{n}/11", fg="green" if n == 11 else "gray")

    entry.bind("<KeyRelease>", atualizar_contador)

    return entry


def tela_login():
    """Exibe a tela inicial para login ou cadastro de conta."""
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="CPF:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
    entry_cpf = campo_cpf(frame, row=1)  # Campo com restrição de 11 dígitos

    def entrar():
        cpf = entry_cpf.get()
        if len(cpf) != 11:
            messagebox.showwarning("CPF inválido", "Digite exatamente 11 números.")
            return
        conta = banco.buscar_conta(cpf)
        if conta:
            global conta_ativa
            conta_ativa = conta
            tela_operacoes()
        else:
            messagebox.showerror("Não encontrado", "CPF não cadastrado.\nClique em 'Cadastrar' para criar uma conta.")

    tk.Button(frame, text="Entrar",    command=entrar,        width=14).grid(row=3, column=0, padx=(0, 4), sticky="ew")
    tk.Button(frame, text="Cadastrar", command=tela_cadastro, width=14).grid(row=3, column=1, padx=(4, 0), sticky="ew")

    janela.title("SisBanco — Login")


def tela_cadastro():
    """Tela para criar uma nova conta."""
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Nome:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(frame, font=("Segoe UI", 11))
    entry_nome.grid(row=1, column=0, columnspan=2, sticky="ew", ipady=6, pady=(2, 8))

    tk.Label(frame, text="CPF:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w")
    entry_cpf = campo_cpf(frame, row=3)  # Campo com restrição de 11 dígitos

    def cadastrar():
        nome = entry_nome.get().strip()
        cpf  = entry_cpf.get()

        if not nome:
            messagebox.showwarning("Atenção", "Preencha o nome.")
            return
        if len(cpf) != 11:
            messagebox.showwarning("CPF inválido", "Digite exatamente 11 números.")
            return

        ok, resultado = banco.criar_conta(nome, cpf)
        if ok:
            messagebox.showinfo("Sucesso", f"Conta criada com sucesso!\nID: {resultado}")
            tela_login()
        else:
            # banco.criar_conta retorna "CPF já cadastrado." quando há duplicata
            messagebox.showerror("CPF já cadastrado", f"O CPF {cpf} já possui uma conta.\nFaça login para acessá-la.")

    tk.Button(frame, text="Criar conta", command=cadastrar ).grid(row=5, column=0, sticky="ew", padx=(0, 4))
    tk.Button(frame, text="Voltar",      command=tela_login).grid(row=5, column=1, sticky="ew", padx=(4, 0))

    janela.title("SisBanco — Cadastro")


def tela_operacoes():
    """Tela principal da conta: depósito, saque, extrato e opções."""
    for widget in frame.winfo_children():
        widget.destroy()

    janela.title(f"SisBanco — {conta_ativa.nome}")

    label_saldo = tk.Label(frame, text="", font=("Segoe UI", 13, "bold"))
    label_saldo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    def atualizar_saldo():
        label_saldo.config(text=f"Saldo: R$ {conta_ativa.saldo:.2f}")

    tk.Label(frame, text="Valor (R$):", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
    entry_valor = tk.Entry(frame, font=("Segoe UI", 11))
    entry_valor.grid(row=2, column=0, columnspan=2, sticky="ew", ipady=6, pady=(2, 10))

    def operacao(tipo):
        """Executa depósito ou saque, salva no banco e atualiza a tela."""
        try:
            valor = float(entry_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
            return
        finally:
            entry_valor.delete(0, tk.END)  # Limpa o campo sempre

        if tipo == "deposito":
            ok, msg = conta_ativa.depositar(valor)
        else:
            ok, msg = conta_ativa.sacar(valor)

        if ok:
            banco.atualizar_conta(conta_ativa)                      # Salva saldo no banco
            banco.registrar_transacao(conta_ativa.id, tipo, valor)  # Registra a transação
            atualizar_saldo()
            carregar_extrato()  # Atualiza o extrato após cada operação

        messagebox.showinfo("Resultado", msg)

    tk.Button(frame, text="Depositar", command=lambda: operacao("deposito")).grid(row=3, column=0, sticky="ew", padx=(0, 4))
    tk.Button(frame, text="Sacar",     command=lambda: operacao("saque")   ).grid(row=3, column=1, sticky="ew", padx=(4, 0))

    tk.Label(frame, text="Extrato:", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=(12, 4))

    texto_extrato = tk.Text(frame, font=("Consolas", 9), state="disabled", height=10)
    texto_extrato.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
    frame.rowconfigure(5, weight=1)

    def carregar_extrato():
        transacoes = banco.extrato(conta_ativa.id)
        texto_extrato.config(state="normal")
        texto_extrato.delete("1.0", tk.END)
        if not transacoes:
            texto_extrato.insert(tk.END, "Sem movimentações.")
        for tipo, valor, data in transacoes:
            simbolo = "▲" if tipo == "deposito" else "▼"
            texto_extrato.insert(tk.END, f"{simbolo} R$ {valor:.2f}  —  {data}\n")
        texto_extrato.config(state="disabled")  # Somente leitura

    carregar_extrato()

    tk.Button(frame, text="Editar nome",    command=tela_editar_nome).grid(row=6, column=0, sticky="ew", padx=(0, 4), pady=(0, 4))
    tk.Button(frame, text="Encerrar conta", command=tela_encerrar   ).grid(row=6, column=1, sticky="ew", padx=(4, 0), pady=(0, 4))
    tk.Button(frame, text="Sair",           command=tela_login       ).grid(row=7, column=0, columnspan=2, sticky="ew")

    atualizar_saldo()


def tela_editar_nome():
    """Tela para atualizar o nome do titular."""
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Novo nome:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(frame, font=("Segoe UI", 11))
    entry_nome.insert(0, conta_ativa.nome)  # Preenche com o nome atual
    entry_nome.grid(row=1, column=0, columnspan=2, sticky="ew", ipady=6, pady=(2, 10))

    def salvar():
        novo_nome = entry_nome.get().strip()
        if not novo_nome:
            messagebox.showwarning("Atenção", "Digite um nome válido.")
            return
        banco.atualizar_nome(conta_ativa.cpf, novo_nome)
        conta_ativa.nome = novo_nome  # Atualiza o objeto em memória também
        messagebox.showinfo("Sucesso", "Nome atualizado.")
        tela_operacoes()

    tk.Button(frame, text="Salvar", command=salvar        ).grid(row=2, column=0, sticky="ew", padx=(0, 4))
    tk.Button(frame, text="Voltar", command=tela_operacoes).grid(row=2, column=1, sticky="ew", padx=(4, 0))

    janela.title("SisBanco — Editar nome")


def tela_encerrar():
    """Confirmação para excluir a conta permanentemente."""
    confirmar = messagebox.askyesno(
        "Encerrar conta",
        f"Tem certeza que deseja encerrar a conta de {conta_ativa.nome}?\nEsta ação não pode ser desfeita."
    )
    if confirmar:
        ok, msg = banco.excluir_conta(conta_ativa.cpf)
        messagebox.showinfo("Resultado", msg)
        if ok:
            tela_login()


# ── Inicialização ─────────────────────────────────────────────────

banco.criar_tabelas()  # Garante que o banco e as tabelas existem antes de qualquer uso

janela = tk.Tk()
janela.title("SisBanco")
janela.resizable(True, True)

w, h = 380, 460
janela.geometry(f"{w}x{h}+{(janela.winfo_screenwidth()-w)//2}+{(janela.winfo_screenheight()-h)//2}")

janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

frame = tk.Frame(janela, padx=20, pady=20)
frame.grid(sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

tela_login()       # Começa pela tela de login
janela.mainloop()