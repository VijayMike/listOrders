from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from typing import List

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(String, default="Pending") 
    product = relationship("ProductDB")

def reset_database():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)  
    populate_sample_data() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    customer_name: str
    product_id: int
    quantity: int
    status: str
    class Config:
        orm_mode = True

def populate_sample_data():
    db = SessionLocal()

    sample_products = [
        ProductDB(name="Laptop", description="High-performance laptop", price=199999.99, category="Electronics"),
        ProductDB(name="Smartphone", description="Latest model smartphone", price=165999.99, category="Electronics"),
        ProductDB(name="Desk Chair", description="Ergonomic office chair", price=7599.99, category="Furniture"),
        ProductDB(name="Coffee Maker", description="Automatic coffee machine", price=3599.99, category="Appliances"),
    ]
    
    db.add_all(sample_products)
    db.commit()

    sample_orders = [
        OrderDB(customer_name="Vijay", product_id=1, quantity=1, status="Pending"),
        OrderDB(customer_name="Mike", product_id=2, quantity=2, status="Shipped"),
        OrderDB(customer_name="Sushmi", product_id=3, quantity=1, status="Delivered"),
        OrderDB(customer_name="Sen", product_id=4, quantity=3, status="Pending"),
    ]
    
    db.add_all(sample_orders)
    db.commit()
    db.close()

reset_database()

@app.get("/products/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/orders/", response_model=List[Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderDB).all()