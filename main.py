from arquivo import *
from crud_db import *
from models import *
from caixa import caixa

# APAGA TODOS OS REGISTROS PARA INICAR DO ZERO
# excluir_todos_produtos_db()
# excluir_todos_clientes_db()

def produtos_csv_para_db():
    produtos = ler_arquivo("produtos.csv")
    # Adicionar produtos no banco de dados
    for produto in produtos:
        adicionar_produto_db(produto)
    produtos_db = consultar_todos_classe_db(Produto)
    return produtos_db

def clientes_csv_para_db():
    clientes = ler_arquivo("clientes.csv")
    # Adicionar clientes ao banco
    for cliente in clientes:
        adicionar_clients_csv_db(cliente)
    clientes_db = consultar_todos_classe_db(Cliente)
    return clientes_db

produtos = produtos_csv_para_db()
clientes = clientes_csv_para_db()

if produtos != []:
    produtos = caixa(produtos, clientes)


'''
para instalar:
sqlalchemy
pymysql
tabulate
pandas
'''
