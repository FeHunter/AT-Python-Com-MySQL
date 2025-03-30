from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)

    compras = relationship("Compra", back_populates="cliente", cascade="all, delete-orphan")

    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f"{self.id_cliente} {self.nome}"
    
class Produto(Base):
    __tablename__ = "produto"
    
    id_produto = Column(Integer, primary_key=True)
    nome = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)

    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = int(quantidade)
        self.preco = float(preco)

    def __str__(self):
        return f"{self.id_produto} {self.nome} {self.quantidade} {self.preco}"

class Compra(Base):
    __tablename__ = "compra"

    id_compra = Column(Integer, primary_key=True)
    data_compra = Column(String)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))

    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("Item", back_populates="compra", cascade="all, delete-orphan")

    def __init__(self, data_compra, id_cliente):
        self.data_compra = data_compra
        self.id_cliente = id_cliente

    def __str__(self):
        return f"{self.id_compra} {self.data_compra} {self.cliente.nome}"
    
class Item(Base):
    __tablename__ = "item"

    id_item = Column(Integer, primary_key=True)
    quantidade = Column(Integer)
    id_compra = Column(Integer, ForeignKey("compra.id_compra"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))

    compra = relationship("Compra", back_populates="itens")
    produto = relationship("Produto")

    def __init__(self, quantidade, id_compra, id_produto):
        self.quantidade = quantidade
        self.id_compra = id_compra
        self.id_produto = id_produto

    def __str__(self):
        return f"{self.id_item} {self.quantidade} {self.compra.id_compra} {self.produto.nome}"
