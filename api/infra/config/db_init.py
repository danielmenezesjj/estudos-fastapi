from sqlalchemy import text
from api.infra.config.database import engine

def run_init_script():
    with engine.connect() as connection:
        print("Executando o script init.sql...")
        check_table_query = """
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
        BEGIN
            CREATE TABLE Products (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                quantity INT,
                price FLOAT NOT NULL
            );
        END

        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
        BEGIN
            CREATE TABLE Orders (
                id INT IDENTITY(1,1) PRIMARY KEY,
                type_pagament VARCHAR(100) NOT NULL,
                quantity INT,
                value FLOAT NOT NULL,
                status VARCHAR(100) NOT NULL,
                id_product INT REFERENCES Products(id)
            );
        END
        """
        connection.execute(text(check_table_query))
        connection.commit()
        print("Tabela Products criada com sucesso ou já existe.")


