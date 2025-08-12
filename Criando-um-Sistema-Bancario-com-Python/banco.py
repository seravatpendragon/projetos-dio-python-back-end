saldo = 0.0
extrato = ""
num_saques = 0
LIMITE_SAQUES = 3
LIMITE_POR_SAQUE = 500

while True:
    print("\n" + "=" * 30)
    print("    SISTEMA BANCÁRIO    ")
    print("=" * 30)
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[4] Sair")
    print("=" * 30)
    
    opcao = input("Escolha uma opção: ")
    
    # Depósito
    if opcao == "1":
        print("\n-> DEPÓSITO")
        valor_str = input("Valor a depositar: R$ ")
        
        # Verifica se o valor é numérico
        if valor_str.replace('.', '', 1).isdigit() and valor_str.count('.') <= 1:
            valor = float(valor_str)
            
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print(f"\nDepósito de R$ {valor:.2f} realizado!")
            else:
                print("\nValor inválido! O valor deve ser positivo.")
        else:
            print("\nValor inválido! Use apenas números (ex: 100.50)")
    
    # Saque
    elif opcao == "2":
        print("\n-> SAQUE")
        
        if num_saques >= LIMITE_SAQUES:
            print("\nLimite diário de saques atingido (3 saques por dia).")
            continue
            
        valor_str = input("Valor a sacar: R$ ")
        
        # Verifica se o valor é numérico
        if valor_str.replace('.', '', 1).isdigit() and valor_str.count('.') <= 1:
            valor = float(valor_str)
            
            if valor > LIMITE_POR_SAQUE:
                print(f"\nLimite máximo por saque é R$ {LIMITE_POR_SAQUE:.2f}!")
            elif valor > saldo:
                print("\nSaldo insuficiente!")
            elif valor <= 0:
                print("\nValor inválido! O valor deve ser positivo.")
            else:
                saldo -= valor
                num_saques += 1
                extrato += f"Saque:    R$ {valor:.2f}\n"
                print(f"\nSaque de R$ {valor:.2f} realizado!")
                print(f"Saques restantes hoje: {LIMITE_SAQUES - num_saques}")
        else:
            print("\nValor inválido! Use apenas números (ex: 50.00)")
    
    # Extrato
    elif opcao == "3":
        print("\n" + "=" * 30)
        print("        EXTRATO        ")
        print("=" * 30)
        
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
            print("-" * 30)
            print(f"Saldo atual: R$ {saldo:.2f}")
        print("=" * 30)
    
    # Sair
    elif opcao == "4":
        print("\nObrigado por usar nosso sistema bancário!")
        break
    
    # Opção inválida
    else:
        print("\nOpção inválida! Por favor escolha 1, 2, 3 ou 4.")