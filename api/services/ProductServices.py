from sqlalchemy import text
from sqlalchemy.orm import Session
from api.infra.config.database import engine


class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_product_by_id(self, product_id: int):
        result = self.db_session.execute(text("SELECT * FROM Products WHERE id = :product_id"), {"product_id": product_id})
        product = result.fetchone()
        print(f"Resultado da consultaaaa: {product}")
        if product is not None:
            column_names = result.keys()
            return dict(zip(column_names, product))
        return None
    
    def get_all_products(self):
        result = self.db_session.execute(text("SELECT * FROM Products"))
        products = result.mappings().all()
        return products
       
    def insert_product(self, name: str, quantity: int, price: float):
        query = text("""
            INSERT INTO Products (name, quantity, price)
            VALUES (:name, :quantity, :price)
        """)
        self.db_session.execute(query, {"name": name, "quantity": quantity, "price": price})
        self.db_session.commit()

    def delete_product(self, product_id: int):
        self.db_session.execute(text("DELETE FROM Products where id = :product_id"), {"product_id": product_id})
        self.db_session.commit()

    def update_product(self, product_id: int, name: str = None, quantity: int = None, price: float = None):
        query = text("UPDATE Products SET")
        updates = []
        params = {}

        if name is not None:
            updates.append(" name = :name")
            params["name"] = name
        
        if quantity is not None:
            updates.append(" quantity = :quantity")
            params["quantity"] = quantity
        
        if price is not None:
            updates.append(" price = :price")
            params["price"] = price
        
        if not updates:
            raise ValueError("Não há dados para atualizar")

        query = text(f"UPDATE Products SET {', '.join(updates)} WHERE id = :product_id")
        print(query)
        params["product_id"] = product_id
        self.db_session.execute(query, params)
        self.db_session.commit()

