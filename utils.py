from datetime import datetime

def msg_iniciar_atendimento ():
    while True:
        resposta = input("\nIniciar atendimento? S|N : ")
        if (resposta.lower() == "s"):
            return True
        elif (resposta.lower() == "n"):
            return False
        else:
            print("Entrada inválida")

def msg_finalizar_atendimento ():
    while True:
        resposta = input("\nFinalizar atendimento? S|N : ")
        if (resposta.lower() == "s"):
            return False
        elif (resposta.lower() == "n"):
            return True
        else:
            print("Entrada inválida")

def msg_fechar_caixa():
    fechar = input("\nFechar o caxia? S/N: ")
    if fechar.lower() == "s":
        return True
    elif fechar.lower() == "n":
        return False
    else:
        print("Entrada inválida")

def entrar_quantidade (produto):
    while True:
        try:
            qtd = int(input("Digite a quantidade do produto: "))
            if (qtd > 0):
                if verificar_estoque(produto, qtd):
                    return qtd
                else:
                    print("Estoque insuficiente")
            else:
                print("A quantidade tem que ser maior que zero")
        except:
            print("Entrada inválida")

def entrar_id (produtos):
    try:
        while True:
            id = int(input("Digite o id do produto: "))
            if pesquisar_id(produtos, id):
                produto = produto_pelo_id(produtos, id)
                print(f'quantidade | {produto.quantidade}')
                if produto.quantidade > 0:
                    return int(id)
                else:
                    print("Produto sem estoque")
    except:
        print("Entrada inválida, ID não localizado.")
    
def pesquisar_id (produtos, id):
    '''
    faz a busca pelo id do produto dentro da lista de produtos, caso encontre retorna o id se não retorna -1
    '''
    for produto in produtos:
        # print(f'id do produto dentro do pesquisar_id: {produto.id_produto} | id digitado: {id}')
        if (int(produto.id_produto) == id):
            return True
    print("Produto não cadastrado")
    return False

def verificar_estoque(produto, quantidade):
    '''
    Recebe o produto e quantidade informada e verificar se o estoque e suficiente
    '''
    if int(produto.quantidade) >= int(quantidade):
        return True
    else:
        return False
            
def remover_produto_estoque (produtos, id, quantidade):
    for produto in produtos:
        if produto.id_produto == id:
            produto['quantidade'] -= quantidade
    return produtos

def produto_pelo_id (produtos, id):
    for produto in produtos:
        if produto.id_produto == id:
            return produto

def imprimir_produtos (produtos):
    print("\nProdutos Disponiveis:")
    for produto in produtos:
        print(f"{produto}")

def msg_informacoes_cliente (client_id):
    print(f"\nCliente {client_id}")
    data_hora = datetime.now()
    data_hora_formatado = data_hora.strftime("%d/%m/%Y %H:%M")
    print(f"Data: {data_hora_formatado}")
