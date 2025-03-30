from tabulate import tabulate
from utils import *
from models import *
from crud_db import *

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
        if produto.id_produto == id_produto:
            print(f"{produto.nome} está sendo adicionado.")
            quantidade = entrar_quantidade(produto)
            produtos = remover_produto_estoque(produtos, id_produto, quantidade)
            
            # Cria um dicionário com os dados do item comprado
            add_produto = {
                'id_produto': produto.id_produto,
                'nome': produto.nome,
                'quantidade': quantidade,
                'preco': produto.preco
            }
            itens_cliente.append(add_produto)
            print(f"{produto.nome} foi adicionado.")
    return produtos, itens_cliente

def listar_clientes(clientes):
    print("\nLista de Clientes:")
    for i, cliente in enumerate(clientes, start=1):
        print(f"{i} - {cliente.nome}")
    print(f"{len(clientes) + 1} - Adicionar Novo Cliente")  # Opção para adicionar novo cliente
    print(f"{len(clientes) + 2} - Fechar Caixa")

def entrar_op_cliente(clientes):
    while True:
        try:
            op = int(input("\nEscolha um cliente para atender: "))
            if 1 <= op <= len(clientes) + 2:
                return op
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

def caixa(produtos, clientes):
    while True:
        listar_clientes(clientes)
        escolha_cliente = entrar_op_cliente(clientes)

        if escolha_cliente == len(clientes) + 1:  # Adicionar novo cliente
            nome_cliente = input("Digite o nome do cliente: ")
            id_novo_cliente = adicionar_cliente_db(nome_cliente)
            clientes = consultar_todos_classe_db(Cliente)  # Atualiza a lista do banco

        if escolha_cliente == len(clientes) + 2:  # Fechar caixa
            mostrar_resumo_caixa()
            mostrar_produtos_sem_estoque(produtos)
            break

        id_cliente = clientes[escolha_cliente - 1].id_cliente
        print(f"\nIniciando atendimento do Cliente {clientes[escolha_cliente - 1].nome}")

        produtos, itens_cliente = controle_caixa(produtos)

        if itens_cliente:
            id_compra = registrar_compra(id_cliente, itens_cliente)
            imprimir_nota_cliente(itens_cliente, id_compra)

        flag = input("\nDeseja atender outro cliente? (s/n): ").lower()
        if flag != 's':
            break

    mostrar_resumo_caixa()
    return produtos

def imprimir_nota_cliente(itens_cliente, id_compra):
    tabela = []
    total_cliente = 0

    for item in itens_cliente:
        id_item = item.get('id_produto')
        nome = item.get('nome')
        quantidade = item.get('quantidade')
        preco = item.get('preco')

        total = quantidade * preco
        tabela.append([id_item, nome, quantidade, preco, total])
        total_cliente += total

    print(f"\nNota do Cliente - Compra ID {id_compra}:")
    print(tabulate(tabela, headers=["Item", "Produto", "Quant.", "Preço", "Total"], tablefmt="grid"))
    print(f"Itens: {len(itens_cliente)}")
    print(f"Total: {total_cliente}\n")

def mostrar_resumo_caixa():
    compras = consultar_todos_classe_db(Compra)
    resumo = []
    total_vendas = 0

    for compra in compras:
        total_cliente = sum(item.produto.preco * item.quantidade for item in compra.itens)
        total_vendas += total_cliente
        resumo.append([f"Cliente {compra.id_cliente}", total_cliente])

    print("\nFechamento do Caixa:")
    print(tabulate(resumo, headers=["Cliente", "Total"], tablefmt="grid"))
    print(f"Total de vendas: {total_vendas}")

def mostrar_produtos_sem_estoque(produtos):
    print("\nProdutos sem estoque:")
    for produto in produtos:
        if int(produto.quantidade) <= 0:
            print(produto.nome)
