from sqlalchemy import text
from sqlalchemy.orm import Session
from api.infra.config.database import engine
from api.services.ProductServices import ProductService

class OrderServices():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
    def get_all_orders(self):
        query = text("""
            SELECT 
                Orders.id AS order_id,
                Orders.quantity AS order_quantity,
                Orders.value AS order_value,
                Orders.status AS order_status,
                Orders.type_pagament AS order_type_pagament,
                Products.id AS product_id,
                Products.name AS product_name,
                Products.quantity AS product_quantity,
                Products.price AS product_price
            FROM 
                Orders
            JOIN 
                Products ON Orders.id_product = Products.id

        """)
        result = self.db_session.execute(query)
        orders = result.mappings().all()
        return orders
    
    def insert_orders(self, id_product: int, quantity: int, value: float, type_pagament: str, status: str):
        service = ProductService(self.db_session)
        product = service.get_product_by_id(id_product)
        
        print(f"Quantidade no banco: {product['quantity']} (tipo: {type(product['quantity'])}), Quantidade no pedido: {quantity} (tipo: {type(quantity)})")

        if int(product['quantity']) < quantity:
            raise ValueError("Não contém quantidade suficiente para realizar esse pedido")
        

        query = text("""
            INSERT INTO Orders (id_product, quantity, value, status, type_pagament)
            VALUES (:id_product, :quantity, :value, :status, :type_pagament)
        """)
        
        self.db_session.execute(query, {
            "id_product": id_product,
            "quantity": quantity,
            "value": value, 
            "status": status,
            "type_pagament": type_pagament
        })
        
        self.db_session.commit()

        
 
