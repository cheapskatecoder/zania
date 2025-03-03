from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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
    total_price = Decimal("0.00")
    order_items = []

    # Extract unique product IDs from order items
    product_ids = {item.product_id for item in order.items}

    # Fetch all products in one go using .in_()
    products = db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()
    products_dict = {product.id: product for product in products}

    # Verify that all requested products exist
    if len(products_dict) != len(product_ids):
        missing_ids = product_ids - set(products_dict.keys())
        missing_id = missing_ids.pop()  # Report one missing product
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {missing_id} not found"
        )

    # Validate stock and calculate total price
    for item in order.items:
        product = products_dict[item.product_id]
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {item.quantity}"
            )

        product_price_decimal = Decimal(str(product.price))
        item_price = product_price_decimal * Decimal(item.quantity)
        total_price += item_price
        order_items.append({"product": product, "quantity": item.quantity})

    try:
        # Create the order
        db_order = models.Order(
            total_price=total_price,
            status=models.OrderStatus.PENDING
        )
        db.add(db_order)
        db.flush()  # Flush to get the order ID

        # Update product stock and add products to the order
        for item in order_items:
            product = item["product"]
            quantity = item["quantity"]

            # Update product stock
            product.stock -= quantity

            # Insert into the association table for order-product
            db.execute(
                models.order_product.insert().values(
                    order_id=db_order.id,
                    product_id=product.id,
                    quantity=quantity
                )
            )

        db.commit()
        db.refresh(db_order)

        # Return the response with total_price cast as a Decimal
        return {
            "id": db_order.id,
            "total_price": Decimal(str(db_order.total_price)),
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
