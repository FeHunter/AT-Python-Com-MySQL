from tabulate import tabulate
from utils import *

def controle_caixa(produtos_disponiveis):
    produtos = produtos_disponiveis
    itens_cliente = []
    flag = msg_iniciar_atendimento()  # Pergunta se quer iniciar o atendimento
    while flag:
        imprimir_produtos(produtos)
        id_produto = entrar_id(produtos)
        produtos, itens_cliente = adicionar_produto(produtos, id_produto, itens_cliente)
        flag = msg_finalizar_atendimento()  # Pergunta se quer finalizar atendimento
    return produtos, itens_cliente

def adicionar_produto(produtos, id_produto, itens_cliente):
    for produto in produtos:
        print(f'id do produto: {produto.id_produto} | id digitado = {id_produto}')
        # Aqui vamos acessar o atributo 'id_produto' diretamente
        if produto.id_produto == id_produto:
            print(f"{produto.nome} está sendo adicionado.")
            quantidade = entrar_quantidade(produto)
            produtos = remover_produto_estoque(produtos, id_produto, quantidade)
            # copia o produto e adiciona ao carrinho
            add_produto = produto.__dict__.copy()  # Copia os dados do produto para a lista
            add_produto['quantidade'] = quantidade  # Adiciona a quantidade ao item
            itens_cliente.append(add_produto)
            print(f"{produto.nome} foi adicionado.")
    return produtos, itens_cliente


def caixa(produtos, clientes):
    contador_clientes = 0
    while True:
        # Pergunta se quer iniciar atendimento para o próximo cliente
        print(f"\nIniciando atendimento do Cliente {contador_clientes + 1}")
        produtos, itens_cliente = controle_caixa(produtos)
        clientes.append(itens_cliente)  # Adiciona o atendimento do cliente
        imprimir_nota_cliente(clientes, contador_clientes)
        contador_clientes += 1
        if not msg_finalizar_atendimento():  # Pergunta se quer continuar o atendimento de mais clientes
            break
    mostrar_resumo_caixa(clientes)
    mostrar_produtos_sem_estoque(produtos)
    return produtos

def imprimir_nota_cliente(clientes, contador_clientes):
    cliente = clientes[contador_clientes]
    tabela = []
    total_cliente = 0
    for item in cliente:
        id_item, nome, quantidade, preco = item
        total = quantidade * preco
        tabela.append([id_item, nome, quantidade, preco, total])
        total_cliente += total

    msg_informacoes_cliente(contador_clientes + 1)
    print(tabulate(tabela, headers=["Item", "Produto", "Quant.", "Preço", "Total"], tablefmt="grid"))
    print(f"Itens: {len(cliente)}")
    print(f"Total: {total_cliente}\n")

def mostrar_resumo_caixa(clientes):
    resumo = []
    total_vendas = 0

    for i in range(0, len(clientes)):
        cliente = clientes[i]
        total_cliente = sum(item[2] * item[3] for item in cliente)
        total_vendas += total_cliente
        resumo.append([f"Cliente: {i+1}", total_cliente])

    print("\nFechamento do Caixa:")
    print(tabulate(resumo, headers=["Cliente", "Total"], tablefmt="grid"))
    print(f"Total de vendas: {total_vendas}")

def mostrar_produtos_sem_estoque(produtos):
    print("\nProdutos sem estoque:")
    for produto in produtos:
        if int(produto[2]) <= 0:
            print(produto[1])
