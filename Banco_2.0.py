import textwrap

# Functionalities
def saque(*, valor, valor_limite_saque, conta,limite_saques):
    if valor <= 0:
        print("O valor do saque deve ser maior que zero.")

    elif valor > valor_limite_saque:
        print("O valor do saque excede o limite permitido")

    elif conta["numero_saques"] >= limite_saques:
        print("O limite de saques diarios foi atingido")

    elif conta["saldo"] <= 0:
        print("Saldo insuficiente!")

    elif conta["saldo"] >= valor:
        conta["saldo"] -= valor
        conta["numero_saques"] += 1
        conta["movimentacoes"].append(f"Saque: -{valor:.2f}")
        print("Saque realizado com sucesso.")

    else:
        print("Operação falhou! O valor informado é inválido...")

def deposito(conta, valor):
    if valor <= 0:
        print("O valor do depósito deve ser maior que zero.")
    
    conta["saldo"] += valor
    conta["movimentacoes"].append(f"Depósito: +{valor:.2f}")
    print("Depósito realizado com sucesso.")

def extrato(*, conta):
    if not conta["movimentacoes"]:
        print("Não há movimentações registradas no extrato.")
        return

    print("\n================ EXTRATO ================")
    print(f"Extrato da conta {conta['numero_conta']} - Agência {conta['agencia']}:")
    for movimentacao in conta["movimentacoes"]:
        print(movimentacao)
    print(f"\nSaldo Disponivel: {conta['saldo']:.2f}")
    print("=========================================")

def cadastrar_cliente(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    
    usuario_existe = verificar_usuario(cpf, usuarios)

    if usuario_existe: 
        print("Já existe um usuário cadastrado com esse CPF.")
        return

    senha = input("Informe uma senha (somente número): ")
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    print("A seguir informe o seu endereço")
    logradouro = input("Informe o seu logradouro")
    numero_casa = int(input("Informe o numero da sua casa: "))
    bairro = input("Informe o seu bairro: ")
    cidade = input("Informe o sua cidade: ")
    estado = input("Informe o seu estado(sigla): ")

    endereco = {
        "logradouro": logradouro,
        "numero_casa": numero_casa,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
    }

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "senha": senha,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print("=== Usuário cadastrado com sucesso! ===")

def abrir_conta(usuario, contas, agencia, tipo_conta_opcoes):
    tipo_conta = int(input("Informe o tipo da conta:\n[1] Poupança\n[2] Corrente\n"))
    tipo_conta_str = tipo_conta_opcoes.buscar(tipo_conta, None)

    numero_conta = f"{tipo_conta_str[0].upper()}{len(contas) + 1:03}"

    if verificar_conta_usuario(usuario["cpf"], tipo_conta_str, contas):
        print("O usuário já possui uma conta desse tipo.")
        return
    
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "tipo_conta": tipo_conta_str,
        "usuario": usuario["cpf"],
        "saldo": 0,
        "movimentacoes": [], 
        "numero_saques": 0
    }

    contas.append(conta)
    print(f"Conta {tipo_conta_str} {numero_conta} aberta com sucesso para o usuário {usuario['nome']}!")

def listar_contas(contas, usuarios):
    for conta in contas:
        usuario = buscar_usuario(conta['usuario'], usuarios)
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Tipo de Conta: {conta['tipo_conta']}")
        print(f"Titular da Conta: {usuario}")
        print("-----------------------")

# Utils
def buscar_conta(cpf, tipo_conta, contas):
    conta_encontrada = next((conta for conta in contas if conta["usuario"] == cpf and conta["tipo_conta"] == tipo_conta), None)

    if conta_encontrada:
        return conta_encontrada
    else:
        return None
    
def verificar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    
    return False

def verificar_conta_usuario(cpf, tipo_conta, contas):
    for conta in contas:
        if conta["usuario"] == cpf and conta["tipo_conta"] == tipo_conta:
            return True
    return False

def buscar_usuario(usuario, usuarios):
    for user in usuarios:
        if user["cpf"] == usuario:
            return user["nome"]

# Screens
def menu_banco():
    menu = """\n
    =========== Sistema Bancário DIO ===========
    [1] \tSacar
    [2] \tDepositar
    [3] \tVisualizar Extrato
    [4] \tNova conta
    [5] \tListar contas
    [6] \tSair
    => """
    return int(input(textwrap.dedent(menu)))

def menu_inicio():
    menu = """\n
    =========== Sistema Bancário DIO ===========
    [1] \tLogin
    [2] \tCadastrar
    [3] \tSair
    => """
    return int(input(textwrap.dedent(menu)))

# Autentication
def login(usuarios):
    cpf = input("Informe o CPF: ")
    senha = input("Informe sua senha: ")
    
    usuario_filtrado = next((usuario for usuario in usuarios if usuario["cpf"] == cpf and usuario["senha"] == senha), None)

    return usuario_filtrado
    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    VALOR_LIMITE_SAQUE_DIARIO = 500

    status_banco = True
    usuario_logado = None

    usuarios = []
    contas = []

    tipo_conta_opcoes = {
        1: "poupança",
        2: "corrente"
    }

    while status_banco:
        opcao = menu_inicio()

        if opcao == 1: # Fazer login
            usuario_logado = login(usuarios)

        elif opcao == 2: # Cadastrar novo cliente
            cadastrar_cliente(usuarios)
            continue

        elif opcao == 3: # Sair da aplicação
            break

        else: 
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        if usuario_logado:
            while True:  # Loop para o menu do banco
                opcao_banco = menu_banco()

                if opcao_banco == 1: # Saque
                    valor_saque = float(input("Informe o valor do saque: "))

                    tipo_conta = int(input("Informe o tipo da conta:\n[1] Poupança\n[2] Corrente\n"))
                    tipo_conta_str = tipo_conta_opcoes.buscar(tipo_conta, None)

                    conta_usuario = buscar_conta(usuario_logado["cpf"], tipo_conta_str, contas)

                    if not conta_usuario:
                        print(f"Não há conta {tipo_conta_str} aberta nesse nome.")
                        continue

                    saque(conta=conta_usuario, valor=valor_saque, valor_limite_saque=VALOR_LIMITE_SAQUE_DIARIO, limite_saques=LIMITE_SAQUES)

                    continue

                elif opcao_banco == 2: # Depositar
                    valor_deposito = float(input("Informe o valor do deposito: "))

                    tipo_conta = int(input("Informe o tipo da conta:\n[1] Poupança\n[2] Corrente\n"))
                    tipo_conta_str = tipo_conta_opcoes.buscar(tipo_conta, None)

                    conta_usuario = buscar_conta(usuario_logado["cpf"], tipo_conta_str, contas)

                    if not conta_usuario:
                        print(f"Não há conta {tipo_conta_str} aberta nesse nome.")
                        continue
                    
                    deposito(conta_usuario, valor_deposito)

                    continue

                elif opcao_banco == 3: # Visualizar Extrato
                    tipo_conta = int(input("Informe o tipo da conta para extrair o extrato:\n[1] Poupança\n[2] Corrente\n"))
                    tipo_conta_str = tipo_conta_opcoes.buscar(tipo_conta, None)

                    conta_usuario = buscar_conta(usuario_logado["cpf"], tipo_conta_str, contas)

                    if not conta_usuario:
                        print(f"Não há conta {tipo_conta_str} aberta nesse nome.")
                        continue

                    extrato(conta=conta_usuario)

                elif opcao_banco == 4: # Nova conta
                    print("=========== Abrir Nova Conta ===========")
                    abrir_conta(usuario_logado, contas, AGENCIA, tipo_conta_opcoes)

                elif opcao_banco == 5: # Listar contas
                    listar_contas(contas, usuarios)
                
                elif opcao_banco == 6: # Sair
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
        else:
            print("Usuario ou senha incorreto!")

main()