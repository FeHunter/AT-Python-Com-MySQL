from conectar_db import *
from models import *
from sqlalchemy import text

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
    """Registra uma compra no banco de dados e associa os itens à compra."""
    try:
        session = conectar()
        
        print("Criando nova compra para o cliente:", id_cliente)  # 🔍 Debug

        nova_compra = Compra(data_compra=obter_data_atual(), id_cliente=id_cliente)
        session.add(nova_compra)
        session.commit()  # 🔍 Garantir que ID da compra seja gerado

        print(f"Compra criada com sucesso! ID: {nova_compra.id_compra}")

        lista_itens = []
        for item in itens_cliente:
            print("Adicionando item:", item)  # 🔍 Verificar se os dados estão corretos

            novo_item = Item(
                quantidade=item["quantidade"],
                id_compra=nova_compra.id_compra,
                id_produto=item["id_produto"]
            )
            session.add(novo_item)
            lista_itens.append(novo_item)

            produto = session.query(Produto).filter_by(id_produto=item["id_produto"]).first()
            if produto:
                produto.quantidade -= item["quantidade"]
                print(f"Estoque atualizado para {produto.nome}: {produto.quantidade}")
            else:
                print(f"Produto ID {item['id_produto']} não encontrado!")

        session.commit()  # 🔍 Este commit é essencial
        print(f"Compra ID {nova_compra.id_compra} e {len(lista_itens)} itens registrados no banco!")

        return nova_compra.id_compra

    except Exception as ex:
        print("Erro ao registrar a compra:", ex)
        session.rollback()
    finally:
        desconectar(session)
