import int
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.infra.repositories.Product_repository import ProductRepository


class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_product_by_id(self, product_id: int):
        repository = ProductRepository(self.db_session)
        return repository.get_by_id(product_id)

    
    def get_all_products(self):
        repository = ProductRepository(self.db_session)
        return repository.get_all()

       
    def insert_product(self, name: str, quantity: int, price: float):
        repository = ProductRepository(self.db_session)
        return repository.insert_procut(name, quantity, price)

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

