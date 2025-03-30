from conectar_db import *
from models import *
from sqlalchemy import text

session = conectar()

def excluir_todos_produtos_db():
    """Apaga todos os produtos do banco de dados."""
    try:
        session = conectar()
        session.query(Produto).delete()
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def excluir_todos_clientes_db():
    """Apaga todos os clientes do banco de dados."""
    try:
        session = conectar()
        session.query(Cliente).delete()
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def adicionar_produto_db(produto):
    """Adiciona um novo produto ao banco de dados."""
    try:
        session = conectar()
        # Resetar ID
        session.execute(text("ALTER TABLE produto AUTO_INCREMENT = 1"))
        session.commit()
        # Adicionar produto
        add_produto = Produto(produto[1], produto[2], produto[3])
        session.add(add_produto)
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def adicionar_clients_csv_db(cliente):
    try:
        session = conectar()
        # Resetar ID
        session.execute(text("ALTER TABLE cliente AUTO_INCREMENT = 1"))
        session.commit()
        # Adicionar cliente
        add_cliente = Cliente(cliente[1])
        session.add(add_cliente)
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def adicionar_cliente_db (nome_cliente):
    """Adiciona um novo cliente ao banco de dados."""
    try:
        session = conectar()
        # Adicionar cliente
        add_cliente = Cliente(nome_cliente)
        session.add(add_cliente)
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def consultar_todos_classe_db(classe):
    """Retorna todos os registros de uma tabela específica."""
    try:
        session = conectar()
        return session.query(classe).all()
    except Exception as ex:
        print(ex)
        return []
    finally:
        desconectar(session)

def registrar_compra(id_cliente, itens_cliente):
    """Registra uma compra na tabela `compra` e adiciona os itens na tabela `item`."""
    try:
        session = conectar()
        # Criar um novo registro de compra
        nova_compra = Compra(id_cliente=id_cliente)
        session.add(nova_compra)
        session.commit()  # Salva para gerar o ID da compra

        # Adicionar os itens comprados na tabela `item`
        for item in itens_cliente:
            novo_item = Item(
                id_compra=nova_compra.id_compra,
                id_produto=item["id_produto"],
                quantidade=item["quantidade"]
            )
            session.add(novo_item)

            # Atualizar a quantidade de produtos no estoque
            produto = session.query(Produto).filter_by(id_produto=item["id_produto"]).first()
            if produto:
                produto.quantidade -= item["quantidade"]

        session.commit()  # Salva todas as mudanças
    except Exception as ex:
        print("Erro ao registrar a compra:", ex)
        session.rollback()
    finally:
        desconectar(session)
