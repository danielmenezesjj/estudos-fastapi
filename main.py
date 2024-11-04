from typing import Union
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.infra.config.database import test_connection
from api.infra.config.db_init import run_init_script
from api.services.ProductServices import ProductService
from api.services.OrderServices import OrderServices
from api.infra.config.database import get_db

app = FastAPI()

test_connection()
run_init_script()





@app.get("/")
def read_root():
    return {"Hello": "World"}   

@app.get("/products")
def read_all_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    products = service.get_all_products()
    return {"products": products}


@app.get("/product/{product_id}")
def read_one_products(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.get_product_by_id(product_id)
    if product is not None:
        return {"product": product}
    return {"erro": "Product not founsd"}


@app.post("/products")
def insert_product(name: str, quantity: int, price: float, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.insert_product(name, quantity, price)
    return {"message": "Product created com successfuly"}

@app.delete("/product/{product_id}")
def delete_one_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.delete_product(product_id)
    return {"message": "Product deleted com successfuly"}


@app.put("/product/{product_id}")
def update_product(product_id: int, name: str = None, quantity: int = None, price: float = None, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.update_product(product_id, name, quantity, price)
    return {"message": "Product updated successfully"}



@app.get("/orders")
def read_all_orders(db: Session = Depends(get_db)):
    service = OrderServices(db)
    orders = service.get_all_orders()
    return {"orders": orders}



@app.post("/orders/")
def create_order(id_product: int, type_pagament: str, value: float, quantity: int, status: str, db: Session = Depends(get_db)):
    order_service = OrderServices(db) 
    order_service.insert_orders(id_product, quantity, value, type_pagament, status)
    return {"message": "Order created successfully"}

