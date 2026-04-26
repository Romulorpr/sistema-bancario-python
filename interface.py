import tkinter as tk
from tkinter import messagebox
import sisbanco


def depositar():
    try:
        valor = float(entrada_valor.get())
        msg = sisbanco.depositar(valor)
        messagebox.showinfo("Depósito", msg)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")
    finally:
        entrada_valor.delete(0, tk.END)  # Limpa o campo após a operação
        atualizar_tela()


def sacar():
    try:
        valor = float(entrada_valor.get())
        msg = sisbanco.sacar(valor)
        messagebox.showinfo("Saque", msg)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")
    finally:
        entrada_valor.delete(0, tk.END)  # Limpa o campo após a operação
        atualizar_tela()


def atualizar_tela():
    label_saldo.config(text=f"Saldo: R$ {sisbanco.ver_saldo():.2f}")
    texto_extrato.config(state="normal")
    texto_extrato.delete("1.0", tk.END)
    texto_extrato.insert(tk.END, sisbanco.ver_extrato())
    texto_extrato.config(state="disabled")  # Impede edição pelo usuário


# Janela principal
janela = tk.Tk()
janela.title("Sistema Bancário")
janela.resizable(True, True)

# Centraliza na tela
w, h = 380, 420
janela.geometry(f"{w}x{h}+{(janela.winfo_screenwidth()-w)//2}+{(janela.winfo_screenheight()-h)//2}")

# Layout responsivo
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

frame = tk.Frame(janela, padx=20, pady=20)
frame.grid(sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(5, weight=1)  # Extrato cresce ao redimensionar

# Campo de valor
tk.Label(frame, text="Valor (R$):").grid(row=0, column=0, columnspan=2, sticky="w")
entrada_valor = tk.Entry(frame, font=("Segoe UI", 11))
entrada_valor.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 12))

# Botões lado a lado
tk.Button(frame, text="Depositar", command=depositar).grid(row=2, column=0, sticky="ew", padx=(0, 4))
tk.Button(frame, text="Sacar", command=sacar).grid(row=2, column=1, sticky="ew", padx=(4, 0))

# Saldo
label_saldo = tk.Label(frame, text="Saldo: R$ 0.00", font=("Segoe UI", 12, "bold"))
label_saldo.grid(row=3, column=0, columnspan=2, pady=12)

# Extrato
tk.Label(frame, text="Extrato:").grid(row=4, column=0, columnspan=2, sticky="w")
texto_extrato = tk.Text(frame, font=("Consolas", 10), state="disabled")
texto_extrato.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

atualizar_tela()
janela.mainloop()