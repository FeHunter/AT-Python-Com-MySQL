from conectar_db import *
from models import *
from sqlalchemy import text

session = conectar()

def excluir_todos_produtos_db ():
    # apagar dados já existente para evitar bug de varios produtos repetidos
    try:
        session = conectar()
        session.query(Produto).delete() 
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def excluir_todos_clientes_db ():
    # apagar dados já existente para evitar bug de varios produtos repetidos
    try:
        session = conectar()
        session.query(Cliente).delete() 
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def adicionar_produto_db (produto):
    try:
        session = conectar()
        # resetar id
        session.execute(text("ALTER TABLE produto AUTO_INCREMENT = 1"))
        session.commit()
        # adicionar produtos
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
        # resetar id
        session.execute(text("ALTER TABLE cliente AUTO_INCREMENT = 1"))
        session.commit()
        # adicionar produtos
        add_cliente = Cliente(cliente[1])
        session.add(add_cliente)
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        desconectar(session)

def consultar_todos_classe_db(classe):
    ''' Passa a classe (ex: Produto, Cliente) e retorna os resultados '''
    try:
        session = conectar()
        return session.query(classe).all()
    except Exception as ex:
        print(ex)
        return []
    finally:
        desconectar(session)

