from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


connection_string = "mssql+pyodbc://sa:#abc123#@192.168.0.14:50101/INTRANET_TESTE?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    return engine

def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexão bem-sucedida!")
    except SQLAlchemyError as e:
        print(f"Erro na conexão: {e}")

test_connection()

