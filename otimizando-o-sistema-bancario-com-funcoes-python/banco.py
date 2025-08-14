AGENCIA = "0001"

def saque(*, conta, valor):
    excedeu_saques = conta['numero_saques'] >= conta['limite_saques']
    excedeu_limite = valor > conta['limite']
    sem_saldo = valor > conta['saldo']

    if excedeu_saques:
        print("Operação falhou! Limite diário de saques atingido.")
    elif excedeu_limite:
        print(f"Operação falhou! Valor excede o limite de R$ {conta['limite']:.2f} por saque.")
    elif sem_saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'].append(f"Saque: R$ {valor:.2f}")
        conta['numero_saques'] += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! Valor inválido.")
    
    return conta

def deposito(conta, valor):
    if valor > 0:
        conta['saldo'] += valor
        conta['extrato'].append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! Valor inválido.")
    
    return conta

def exibir_extrato(conta):
    print("\n==================== EXTRATO ====================")
    print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']}")
    print(f"Titular: {conta['usuario']['nome']}\n")
    
    if not conta['extrato']:
        print("Não foram realizadas movimentações.")
    else:
        for movimentacao in conta['extrato']:
            print(movimentacao)
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print("=================================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("CPF já cadastrado! Operação cancelada.")
        return None
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    novo_usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    
    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")
    return novo_usuario

def criar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    
    if not usuario:
        print("Usuário não encontrado! Operação cancelada.")
        return None
    
    nova_conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0.0,
        'limite': 500,
        'extrato': [],
        'numero_saques': 0,
        'limite_saques': 3
    }
    
    return nova_conta

def listar_contas(contas):
    for conta in contas:
        linha = f"""
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
CPF:\t\t{conta['usuario']['cpf']}
Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print(linha)
        print("-" * 40)

def buscar_conta_por_cpf(contas, cpf):
    return [conta for conta in contas if conta['usuario']['cpf'] == cpf]

def main():
    usuarios = []
    contas = []
    proximo_numero_conta = 1
    
    menu = """
    [1] Criar usuário
    [2] Criar conta corrente
    [3] Listar contas
    [4] Depositar
    [5] Sacar
    [6] Extrato
    [7] Sair
    => """
    
    while True:
        opcao = input(menu)
        
        if opcao == "1":  # Criar usuário
            criar_usuario(usuarios)
        
        elif opcao == "2":  # Criar conta corrente
            conta = criar_conta_corrente(AGENCIA, proximo_numero_conta, usuarios)
            if conta:
                contas.append(conta)
                proximo_numero_conta += 1
                print("Conta criada com sucesso!")
        
        elif opcao == "3":  # Listar contas
            listar_contas(contas)
        
        elif opcao == "4":  # Depositar
            cpf = input("CPF do titular: ")
            contas_titular = buscar_conta_por_cpf(contas, cpf)
            
            if not contas_titular:
                print("Nenhuma conta encontrada para este CPF!")
                continue
            
            if len(contas_titular) > 1:
                print("\nContas encontradas:")
                for i, conta in enumerate(contas_titular):
                    print(f"[{i}] Ag: {conta['agencia']} C/C: {conta['numero_conta']}")
                conta_idx = int(input("Selecione o número da conta: "))
                conta_alvo = contas_titular[conta_idx]
            else:
                conta_alvo = contas_titular[0]
            
            valor = float(input("Valor do depósito: R$ "))
            deposito(conta_alvo, valor)
        
        elif opcao == "5":  # Sacar
            cpf = input("CPF do titular: ")
            contas_titular = buscar_conta_por_cpf(contas, cpf)
            
            if not contas_titular:
                print("Nenhuma conta encontrada para este CPF!")
                continue
            
            if len(contas_titular) > 1:
                print("\nContas encontradas:")
                for i, conta in enumerate(contas_titular):
                    print(f"[{i}] Ag: {conta['agencia']} C/C: {conta['numero_conta']}")
                conta_idx = int(input("Selecione o número da conta: "))
                conta_alvo = contas_titular[conta_idx]
            else:
                conta_alvo = contas_titular[0]
            
            valor = float(input("Valor do saque: R$ "))
            saque(conta=conta_alvo, valor=valor)
        
        elif opcao == "6":  # Extrato
            cpf = input("CPF do titular: ")
            contas_titular = buscar_conta_por_cpf(contas, cpf)
            
            if not contas_titular:
                print("Nenhuma conta encontrada para este CPF!")
                continue
            
            if len(contas_titular) > 1:
                print("\nContas encontradas:")
                for i, conta in enumerate(contas_titular):
                    print(f"[{i}] Ag: {conta['agencia']} C/C: {conta['numero_conta']}")
                conta_idx = int(input("Selecione o número da conta: "))
                conta_alvo = contas_titular[conta_idx]
            else:
                conta_alvo = contas_titular[0]
            
            exibir_extrato(conta_alvo)
        
        elif opcao == "7":  # Sair
            print("Obrigado por usar nosso sistema bancário!")
            break
        
        else:
            print("Opção inválida! Por favor selecione uma opção válida.")

if __name__ == "__main__":
    main()