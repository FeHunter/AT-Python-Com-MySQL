from conectar_db import *
from models import *
from sqlalchemy import text
from utils import *

session = conectar()

def excluir_todos_produtos_db():
    """Apaga todos os produtos, itens e compras associadas no banco de dados."""
    try:
        session = conectar()

        # Desabilitar o modo de atualização segura
        session.execute(text('SET SQL_SAFE_UPDATES = 0'))

        # Excluir todos os itens
        session.execute(text('DELETE FROM Item'))
        session.commit()

        # Excluir todas as compras
        session.execute(text('DELETE FROM Compra'))
        session.commit()

        # Excluir todos os produtos
        session.execute(text('DELETE FROM Produto'))
        session.commit()

        # Resetar o auto incremento das tabelas
        session.execute(text('ALTER TABLE Produto AUTO_INCREMENT = 1'))
        session.execute(text('ALTER TABLE Item AUTO_INCREMENT = 1'))
        session.execute(text('ALTER TABLE Compra AUTO_INCREMENT = 1'))
        session.commit()

    except Exception as ex:
        print(f"Erro ao excluir produtos: {ex}")
    finally:
        desconectar(session)

def excluir_todos_clientes_db():
    """Apaga todos os clientes e seus registros associados no banco de dados."""
    try:
        session = conectar()

        # Desabilitar o modo de atualização segura
        session.execute(text('SET SQL_SAFE_UPDATES = 0'))

        # Excluir todos os registros de clientes
        session.execute(text('DELETE FROM Cliente'))
        session.commit()

        # Resetar o auto incremento das tabelas
        session.execute(text('ALTER TABLE Cliente AUTO_INCREMENT = 1'))
        session.commit()

    except Exception as ex:
        print(f"Erro ao excluir clientes: {ex}")
    finally:
        desconectar(session)

def verificar_quantidade_na_tabela (session, verificar_classe):
    ''' Verifica quantidade minica para ver se adiciona ou não os itens do csv '''
    return session.query(verificar_classe).count()

def adicionar_produto_db(produto):
    """Adiciona um novo produto ao banco de dados."""
    try:
        session = conectar()
        qtd = verificar_quantidade_na_tabela(session, Produto)
        if qtd <= 4:
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
        qtd = verificar_quantidade_na_tabela(session, Cliente)
        if qtd <= 2:
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
        clientes_atualizados = consultar_todos_classe_db(Cliente)
        return clientes_atualizados

def atualizar_produtos_db(produtos):
    """Atualizar produtos no banco"""
    try:
        session = conectar()
        for produto in produtos:
            produto_db = session.get(Produto, produto.id_produto)
            if produto_db:
                produto_db.quantidade = produto.quantidade  # Atualiza a quantidade
        session.commit()
    except Exception as ex:
        print(f"Erro ao atualizar os produtos: {ex}")
    finally:
        desconectar(session)

def consultar_todos_classe_db(classe):
    """Retorna todos os registros de uma tabela"""
    try:
        session = conectar()
        return session.query(classe).all()
    except Exception as ex:
        print(ex)
        return []
    finally:
        desconectar(session)

def registrar_compra(id_cliente, itens_cliente):
    nova_compra = Compra(data_compra=obter_data_atual(), id_cliente=id_cliente)
    session.add(nova_compra)
    session.commit()  # Commit inicial para garantir que a compra tenha um ID gerado

    for item in itens_cliente:
        if isinstance(item, dict):  # Verificar se 'item' é um dicionário válido
            novo_item = Item(
                quantidade=item['quantidade'],
                id_compra=nova_compra.id_compra,
                id_produto=item['id_produto']
            )
            session.add(novo_item)

            # Carregar o produto da base de dados e garantir que o objeto está sendo rastreado pela sessão
            produto = session.query(Produto).filter_by(id_produto=item['id_produto']).first()
            
            if produto:
                produto.quantidade -= item['quantidade']  # Diminuir a quantidade do estoque
                
                # Confirmar que o produto foi modificado antes de persistir
                session.add(produto)  # Re-adicionar o produto à sessão para garantir que a mudança seja registrada
                session.commit()  # Persistir a alteração da quantidade
            else:
                print(f"Produto {item['id_produto']} não encontrado!")

        else:
            print(f"Item {item} não é um dicionário válido!")

    session.commit()  # Commit final para registrar todos os itens na compra
    print("Compra registrada com sucesso!")
    return nova_compra.id_compra


