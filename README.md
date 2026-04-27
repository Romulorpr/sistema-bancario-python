# SisBanco — 
Sistema Bancário com Python & Tkinter
Este é um projeto de sistema bancário desenvolvido em Python, utilizando SQLite para persistência de dados e Tkinter para a interface gráfica. O sistema permite o gerenciamento completo de contas, incluindo cadastro, operações de depósito, saque e visualização de extrato em tempo real.

## Funcionalidades

Gestão de Usuários:

• Cadastro de novas contas com validação de CPF (11 dígitos).
• Login seguro por CPF.
• Edição de nome do titular.
• Encerramento definitivo de conta.

Operações Bancárias:

• Depósitos e saques com atualização imediata de saldo.
• Regras de negócio aplicadas: limite de R$ 500,00 por saque e máximo de 3 saques por sessão.

Histórico e Persistência:

• Banco de dados SQLite integrado para salvar contas e transações.
• Extrato detalhado exibindo tipo de operação (▲/▼), valor e data/hora.

## Estrutura

```
sisbanco/
├── main.py        # Ponto de entrada
├── conta.py       # Classe Conta com regras de negócio
├── banco.py       # CRUD e acesso ao SQLite
├── interface.py   # Interface gráfica com tkinter
├── dados.db       # Banco de dados (gerado automaticamente)
└── README.md
```

## Como executar

```
bash
python main.py
```

> Nenhuma dependência externa. Usa apenas bibliotecas da biblioteca padrão do Python (tkinter, sqlite3).

## Tecnologias

•  Python 3
•  tkinter — interface gráfica
•  sqlite3 — persistência de dados

## 🔧 Como Executar

Certifique-se de ter o Python instalado em sua máquina.

Clone este repositório:

• Bash
```
git clone https://github.com/seu-usuario/sistema-bancario-python.git
```

Navegue até a pasta do projeto:

• Bash
```
cd sistema-bancario-python
```

Execute o arquivo principal:

• Bash
```
python main.py
```

## Regras de Negócio Implementadas

Saques:

• Não é possível sacar valores negativos ou maiores que o saldo disponível.
• Existe um limite máximo de R$ 500,00 por operação de saque.
• O usuário pode realizar no máximo 3 saques durante a sessão ativa.

Depósitos:

• Apenas valores positivos são aceitos.

Banco de Dados:

• O arquivo dados.db é criado automaticamente na primeira execução do sistema.

Este projeto foi desenvolvido para fins de estudo sobre integração de interfaces gráficas com bancos de dados relacionais em Python.

## Autor

Romulo - Romulorp

## Versão

v1.0 - Versão inicial com operações básicas

v2.0 - Versão com interface grafica.

v3.0 - Versão final com SQLite e CRUD completo

