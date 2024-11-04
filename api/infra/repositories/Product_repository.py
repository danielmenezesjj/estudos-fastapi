from sqlalchemy import text
from sqlalchemy.orm import Session


class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_by_id(self, id_product: int):
        result = self.db_session.execute(text("SELECT * FROM Products WHERE id = :id_product"),{"id_product": id_product})
        product = result.fetchone()
        if product is not None:
            column_names = result.keys()
            return dict(zip(column_names, product))
        return None

    def get_all(self):
        result = self.db_session.execute(text("SELECT * FROM Products"))
        products = result.mappings().all()
        return products

    def insert_procut(self, name: str, quantity: int, price: float):
        query = text("""
                    INSERT INTO Products (name, quantity, price)
                    VALUES (:name, :quantity, :price)
                """)
        self.db_session.execute(query, {"name": name, "quantity": quantity, "price": price})
        self.db_session.commit()