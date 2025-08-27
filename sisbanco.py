# Variáveis globais para armazenar o estado do sistema bancário
saldo = 0  # Saldo inicial da conta
limite = 500  # Limite máximo por saque
extrato = ""  # String para armazenar o histórico de transações
numero_saques = 0  # Contador de saques realizados no dia
LIMITE_SAQUES = 3  # Limite máximo de saques por dia

# Menu de opções do sistema
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Loop principal do sistema
while True:
    # Exibe o menu e obtém a opção do usuário
    opcao = input(menu)

    # Operação de Depósito
    if opcao == "d":
        try:
            # Solicita o valor do depósito
            valor = float(input("Informe o valor do depósito: "))
            
            # Verifica se o valor é positivo
            if valor > 0:
                # Atualiza o saldo
                saldo += valor
                # Registra a transação no extrato
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")
        except ValueError:
            print("Operação falhou! Por favor, digite um valor numérico válido.")

    # Operação de Saque
    elif opcao == "s":
        try:
            # Solicita o valor do saque
            valor = float(input("Informe o valor do saque: "))
            
            # Verifica as condições para o saque
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES
            
            # Validações das regras de saque
            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite de R$ 500,00.")
            elif excedeu_saques:
                print("Operação falhou! Número máximo de 3 saques diários excedido.")
            elif valor > 0:
                # Executa o saque se todas as condições forem atendidas
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")
        except ValueError:
            print("Operação falhou! Por favor, digite um valor numérico válido.")

    # Operação de Extrato
    elif opcao == "e":
        # Cabeçalho do extrato
        print("\n================ EXTRATO ================")
        
        # Verifica se há transações para exibir
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)  # Exibe todas as transações
        
        # Exibe o saldo atual formatado
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    # Opção para sair do sistema
    elif opcao == "q":
        print("Obrigado por utilizar nossos serviços!")
        break  # Encerra o loop e finaliza o programa

    # Tratamento para opções inválidas
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        