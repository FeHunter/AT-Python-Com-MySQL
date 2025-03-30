from arquivo import *
from crud_db import *
from models import *
from caixa import caixa

produtos = ler_arquivo("produtos.csv")
clientes = ler_arquivo("clientes.csv")

# Adicionar produtos no banco de dados
excluir_todos_produtos_db()
for produto in produtos:
    adicionar_produto_db(produto)
# Adicionar clientes ao banco
excluir_todos_clientes_db()
for cliente in clientes:
    adicionar_clients_csv_db(cliente)

# verificar produtos
consultar_classe_db(Produto)
# verificar clientes
consultar_classe_db(Cliente)


# if produtos != []:
#     produtos = caixa(produtos)
# gravar_arquivo(produtos)

# instalar python-tabulate para o programa funcionar: pip install tabulate