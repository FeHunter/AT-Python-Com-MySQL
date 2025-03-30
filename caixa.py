from tabulate import tabulate
from utils import *
from models import *
from crud_db import *

# A sessão do banco de dados
session = conectar()

# função principal
def caixa(produtos, clientes):
    while True:
        listar_clientes(clientes)
        escolha_cliente = entrar_op_cliente(clientes)

        # Adicionar novo cliente
        if escolha_cliente == len(clientes) + 1:
            nome_cliente = input("Digite o nome do cliente: ")
            adicionar_cliente_db(nome_cliente)
            clientes = consultar_todos_classe_db(Cliente)  # Atualiza a lista do banco

        # Fechar caixa
        if escolha_cliente == len(clientes) + 2:
            break

        # selecionar cliente na lista
        id_cliente = clientes[escolha_cliente - 1].id_cliente
        print(f"\nIniciando atendimento do Cliente {clientes[escolha_cliente - 1].nome}")

        produtos, itens_cliente = controle_caixa(produtos)

        if itens_cliente:
            id_compra = registrar_compra(id_cliente, itens_cliente)
            imprimir_nota_cliente(itens_cliente, id_compra)

        flag = input("\nDeseja atender outro cliente? (s/n): ").lower()
        if flag != 's':
            break

    mostrar_resumo_caixa(produtos)
    mostrar_produtos_sem_estoque(produtos)

def controle_caixa(produtos_disponiveis):
    produtos = produtos_disponiveis
    itens_cliente = []
    flag = msg_iniciar_atendimento()  # Pergunta se quer iniciar o atendimento
    while flag:
        imprimir_produtos(produtos)
        id_produto = entrar_id(produtos)
        produtos, itens_cliente = adicionar_produto(produtos, id_produto, itens_cliente)
        flag = msg_finalizar_atendimento()  # Pergunta se quer finalizar atendimento
    
    # atualizar produtos no banco 
    atualizar_produtos_db(produtos)
    return produtos, itens_cliente # infelizmente preciso retorna os dois aqui, não conseguir pensar em um jeito mais facil pra não retorna dois valres

def adicionar_produto(produtos, id_produto, itens_cliente):
    for produto in produtos:
        if produto.id_produto == id_produto:
            print(f"{produto.nome} esta sendo adicionado.")
            quantidade = entrar_quantidade(produto)
            
            # Verificar o estoque
            if quantidade > produto.quantidade:
                print(f"Quantidade solicitada para {produto.nome} e maior que o estoque disponível.")
                return produtos, itens_cliente
            
            # remove quantidade do estoque
            produto.quantidade -= quantidade
            
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

def registrar_compra(id_cliente, itens_cliente):
    nova_compra = Compra(obter_data_atual(), id_cliente)
    session.add(nova_compra)
    session.commit()

    for item in itens_cliente:
        # Verificar se 'item' é um dicionário antes de tentar acessar as chaves
        if isinstance(item, dict):
            novo_item = Item(
                quantidade=item['quantidade'],
                id_compra=nova_compra.id_compra,
                id_produto=item['id_produto']
            )
            session.add(novo_item)
        else:
            print(f"Erro: {item} não esta correto em formato de dicionario")

    session.commit()
    print("Compra registrada com sucesso!")
    return nova_compra.id_compra

def imprimir_nota_cliente(itens_cliente, id_compra):
    tabela = []
    total_cliente = 0

    for item in itens_cliente:
        if isinstance(item, dict):  # Verificar se é um dicionário antes de acessar
            id_item = item.get('id_produto')
            nome = item.get('nome')
            quantidade = item.get('quantidade')
            preco = item.get('preco')

            total = quantidade * preco
            tabela.append([id_item, nome, quantidade, preco, total])
            total_cliente += total
        else:
            print(f"Erro: {item} não esta correto em formato de dicionario")

    print(f"\nNota do Cliente - Compra ID {id_compra}:")
    print(tabulate(tabela, headers=["Item", "Produto", "Quant.", "Preço", "Total"], tablefmt="grid"))
    print(f"Itens: {len(itens_cliente)}")
    print(f"Total: {total_cliente}\n")

def mostrar_resumo_caixa(produtos):
    compras = consultar_todos_classe_db(Compra)
    resumo = []
    total_vendas = 0

    for compra in compras:
        for item in compra.itens:
            produto = buscar_produto_por_id(item.id_produto, produtos)  # Busca o produto
            total_cliente = produto.preco * item.quantidade
            total_vendas += total_cliente
            resumo.append([f"Cliente {compra.id_cliente}", total_cliente])

    print("\nFechamento do Caixa:")
    print(tabulate(resumo, headers=["Cliente", "Total"], tablefmt="grid"))
    print(f"Total de vendas: {total_vendas}")

def buscar_produto_por_id(id_produto, produtos):
    for produto in produtos:
        if produto.id_produto == id_produto:
            return produto
    return None  # Caso o produto não seja encontrado

def mostrar_produtos_sem_estoque(produtos):
    print("\nProdutos sem estoque:")
    for produto in produtos:
        if int(produto.quantidade) <= 0:
            print(produto.nome)

# Função para carregar compras com itens e produtos relacionados
def consultar_compras_com_produtos():
    return session.query(Compra).all()
