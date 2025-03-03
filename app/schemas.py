from pydantic import BaseModel, validator
from typing import List
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('stock')
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Stock must be non-negative')
        return v

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    product: Product
    quantity: int
    
    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    total_price: float
    status: OrderStatus
    items: List[OrderItem]
    
    class Config:
        orm_mode = True 