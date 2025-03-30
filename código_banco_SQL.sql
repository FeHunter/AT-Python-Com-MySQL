CREATE DATABASE produtos;
use produtos;

DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS compra;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS cliente;

CREATE TABLE cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome NVARCHAR(50) NOT NULL
);

CREATE TABLE produto (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome NVARCHAR(50) NOT NULL,
    quantidade INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

CREATE TABLE compra (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    data_compra DATE NOT NULL,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE item (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    quantidade INT NOT NULL,
    id_compra INT NOT NULL,
    id_produto INT NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);
