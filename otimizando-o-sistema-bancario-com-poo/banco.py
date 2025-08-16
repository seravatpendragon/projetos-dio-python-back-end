from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
    
    def gerar_relatorio(self):
        for transacao in self._transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        conta.saldo -= self.valor
        conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido!")
            return False
        
        if valor > self.saldo:
            print("Saldo insuficiente!")
            return False
        
        self.saldo -= valor
        return True
    
    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido!")
            return False
        
        self.saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0
    
    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.saques_realizados >= self.limite_saques
        
        if excedeu_limite:
            print(f"Valor excede o limite de R$ {self.limite:.2f} por saque!")
            return False
        
        if excedeu_saques:
            print("Limite diário de saques atingido!")
            return False
        
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False

def menu():
    print("\n===== SISTEMA BANCÁRIO =====")
    print("[1] Criar Usuário")
    print("[2] Criar Conta Corrente")
    print("[3] Listar Contas")
    print("[4] Depositar")
    print("[5] Sacar")
    print("[6] Extrato")
    print("[7] Sair")
    return input("=> ")

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":  # Criar Usuário
            cpf = input("CPF (somente números): ")
            
            if any(cliente.cpf == cpf for cliente in clientes):
                print("CPF já cadastrado!")
                continue
            
            nome = input("Nome completo: ")
            data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
            
            novo_cliente = PessoaFisica(cpf, nome, data_nasc, endereco)
            clientes.append(novo_cliente)
            print("Usuário criado com sucesso!")
        
        elif opcao == "2":  # Criar Conta
            cpf = input("CPF do titular: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            
            if not cliente:
                print("Usuário não encontrado!")
                continue
            
            numero_conta = len(contas) + 1
            nova_conta = ContaCorrente(numero_conta, cliente)
            cliente.adicionar_conta(nova_conta)
            contas.append(nova_conta)
            print(f"Conta {numero_conta} criada com sucesso!")
        
        elif opcao == "3":  # Listar Contas
            for conta in contas:
                print(f"\nAgência: {conta.agencia}")
                print(f"C/C: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")
                print(f"Saldo: R$ {conta.saldo:.2f}")
        
        elif opcao == "4":  # Depositar
            numero_conta = int(input("Número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            
            if not conta:
                print("Conta não encontrada!")
                continue
            
            valor = float(input("Valor do depósito: R$ "))
            deposito = Deposito(valor)
            conta.cliente.realizar_transacao(conta, deposito)
            print("Depósito realizado!")
        
        elif opcao == "5":  # Sacar
            numero_conta = int(input("Número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            
            if not conta:
                print("Conta não encontrada!")
                continue
            
            valor = float(input("Valor do saque: R$ "))
            saque = Saque(valor)
            conta.cliente.realizar_transacao(conta, saque)
            print("Saque realizado!")
        
        elif opcao == "6":  # Extrato
            numero_conta = int(input("Número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            
            if not conta:
                print("Conta não encontrada!")
                continue
            
            print("\n===== EXTRATO =====")
            conta.historico.gerar_relatorio()
            print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
            print("===================")
        
        elif opcao == "7":  # Sair
            print("Sistema encerrado!")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()