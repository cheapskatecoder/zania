from decimal import Decimal
from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, Field, validator
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class ProductBase(BaseModel):
    name: str
    description: str
    price: Annotated[Decimal, Field(strict=True, gt=0)]
    stock: int

    @validator('price', pre=True)
    def quantize_price(cls, v):
        try:
            d = Decimal(v)
        except Exception as e:
            raise ValueError("Invalid decimal value") from e
        # Enforce exactly 2 decimal places
        return d.quantize(Decimal("0.01"))

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
    total_price: Annotated[Decimal, Field(strict=True, gt=0)]
    status: OrderStatus
    items: List[OrderItem]
    
    class Config:
        orm_mode = True 
