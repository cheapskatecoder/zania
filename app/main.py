from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import models, schemas
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

@app.get("/products", response_model=List[schemas.Product], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all available products.
    """
    products = db.query(models.Product).all()
    return products

@app.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Add a new product to the platform.
    """
    try:
        db_product = models.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@app.post("/orders", response_model=schemas.Order, status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Place an order for a list of selected products.
    Validates stock availability for each product.
    """
    # Check stock availability and calculate total price
    total_price = 0.0
    order_items = []
    
    # Validate products and collect data for order
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {item.quantity}"
            )
        
        total_price += product.price * item.quantity
        order_items.append({"product": product, "quantity": item.quantity})
    
    try:
        # Create the order
        db_order = models.Order(
            total_price=total_price,
            status=models.OrderStatus.PENDING
        )
        db.add(db_order)
        db.flush()  # Flush to get the order ID
        
        # Update stock and add products to order
        for item in order_items:
            product = item["product"]
            quantity = item["quantity"]
            
            # Update product stock
            product.stock -= quantity
            
            # Add product to order with quantity
            db.execute(
                models.order_product.insert().values(
                    order_id=db_order.id,
                    product_id=product.id,
                    quantity=quantity
                )
            )
        
        # Commit all changes
        db.commit()
        db.refresh(db_order)
        
        # Manually build response since our model doesn't match exactly with the schema
        return {
            "id": db_order.id,
            "total_price": db_order.total_price,
            "status": db_order.status,
            "items": [
                {"product": product, "quantity": quantity}
                for product, quantity in [(item["product"], item["quantity"]) for item in order_items]
            ]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
