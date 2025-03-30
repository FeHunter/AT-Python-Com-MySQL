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
        # Aqui vamos acessar o atributo 'id_produto' diretamente
        if produto.id_produto == id_produto:
            print(f"{produto.nome} está sendo adicionado.")
            quantidade = entrar_quantidade(produto)
            produtos = remover_produto_estoque(produtos, id_produto, quantidade)
            # Copia os dados do produto para a lista
            add_produto = produto.__dict__.copy()  
            add_produto['quantidade'] = quantidade  # Adiciona a quantidade ao item
            itens_cliente.append(add_produto)
            print(f"{produto.nome} foi adicionado.")
    return produtos, itens_cliente

def listar_clientes(clientes):
    print("\nLista de Clientes:")
    for i, cliente in enumerate(clientes, start=1):
        print(f"{i}. Cliente {i}")
    print(f"{len(clientes) + 1}. Fechar Caixa")

def caixa(produtos, clientes):
    caixa_atendimentos = []  # Lista para armazenar todos os atendimentos realizados
    
    while True:
        # Exibe a lista de clientes e opções
        listar_clientes(clientes)
        
        escolha_cliente = int(input("\nEscolha um cliente para atender ou '0' para fechar o caixa: "))
        
        if escolha_cliente == len(clientes) + 1:  # Fechar caixa
            mostrar_resumo_caixa(caixa_atendimentos)  # Passa a lista de atendimentos para o resumo
            mostrar_produtos_sem_estoque(produtos)
            break
        
        if escolha_cliente > len(clientes):  # Entrada inválida
            print("Opção inválida. Tente novamente.")
            continue
        
        # Inicia o atendimento para o cliente escolhido
        print(f"\nIniciando atendimento do Cliente {escolha_cliente}")
        produtos, itens_cliente = controle_caixa(produtos)
        clientes[escolha_cliente - 1] = itens_cliente  # Atualiza o atendimento do cliente existente
        
        caixa_atendimentos.append(itens_cliente)  # Adiciona o atendimento do cliente à lista de atendimentos
        imprimir_nota_cliente(itens_cliente)  # Imprime a nota do cliente
        print("\nAtendimento finalizado!")
        
        flag = input("\nDeseja atender outro cliente? (s/n): ").strip().lower()
        if flag != 's':
            break

    mostrar_resumo_caixa(caixa_atendimentos)  # Exibe o resumo ao final
    return produtos

def imprimir_nota_cliente(itens_cliente):
    tabela = []
    total_cliente = 0
    for item in itens_cliente:
        # Agora acessamos os dados através das chaves do dicionário
        id_item = item.get('id_produto')  # Substituindo pelo nome correto da chave
        nome = item.get('nome')
        quantidade = item.get('quantidade')
        preco = item.get('preco')
        
        total = quantidade * preco
        tabela.append([id_item, nome, quantidade, preco, total])
        total_cliente += total

    print("\nNota do Cliente:")
    print(tabulate(tabela, headers=["Item", "Produto", "Quant.", "Preço", "Total"], tablefmt="grid"))
    print(f"Itens: {len(itens_cliente)}")
    print(f"Total: {total_cliente}\n")

def mostrar_resumo_caixa(caixa_atendimentos):
    resumo = []
    total_vendas = 0

    for i, cliente in enumerate(caixa_atendimentos, start=1):
        total_cliente = sum(item['quantidade'] * item['preco'] for item in cliente)  # Acesso correto aos dados
        total_vendas += total_cliente
        resumo.append([f"Cliente {i}", total_cliente])

    print("\nFechamento do Caixa:")
    print(tabulate(resumo, headers=["Cliente", "Total"], tablefmt="grid"))
    print(f"Total de vendas: {total_vendas}")

def mostrar_produtos_sem_estoque(produtos):
    print("\nProdutos sem estoque:")
    for produto in produtos:
        if int(produto[2]) <= 0:
            print(produto[1])

