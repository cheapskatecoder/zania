from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()

# Association table for the many-to-many relationship between Order and Product
order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer, nullable=False)
)

class OrderStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    
    orders = relationship("Order", secondary=order_product, back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False)
    status = Column(String, default=OrderStatus.PENDING)
    
    products = relationship("Product", secondary=order_product, back_populates="orders") 