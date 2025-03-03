import os
from decimal import Decimal, ROUND_UP

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base, Product

# Test database configuration
TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER", "postgres")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD", "postgres")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB", "test_ecommerce")
TEST_POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST", "db")
TEST_POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT", "5432")

SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # Create test database
    Base.metadata.create_all(bind=engine)
    yield
    # Drop test database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_get_products_empty(client):
    """Test getting products when the database is empty."""
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product(client):
    """Test creating a new product."""
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": "19.99",
        "stock": 100
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]
    assert "id" in data

def test_get_products_after_create(client):
    """Test getting products after creating one."""
    # Create a product first
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "stock": 100
    }
    client.post("/products", json=product_data)
    
    # Get all products
    response = client.get("/products")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == product_data["name"]

def test_create_product_invalid_data(client):
    """Test creating a product with invalid data."""
    # Negative price
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": -19.99,
        "stock": 100
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422  # Validation error

    # Negative stock
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "stock": -10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422  # Validation error

def test_create_order_success(client, test_db):
    """Test creating a successful order."""
    # First, create a product
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "stock": 100
    }
    product_response = client.post("/products", json=product_data)
    product_id = product_response.json()["id"]
    
    # Then, create an order for that product
    order_data = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 5
            }
        ]
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    assert Decimal(data["total_price"]) == (Decimal(product_data["price"]) * Decimal(5)).quantize(Decimal("0.01"), rounding=ROUND_UP)
    assert data["status"] == "pending"
    assert len(data["items"]) == 1
    
    # Check that the stock was updated
    product_in_db = test_db.query(Product).filter(Product.id == product_id).first()
    assert product_in_db.stock == product_data["stock"] - 5

def test_create_order_insufficient_stock(client):
    """Test creating an order with insufficient stock."""
    # First, create a product with limited stock
    product_data = {
        "name": "Limited Stock Product",
        "description": "This product has limited stock",
        "price": 29.99,
        "stock": 3
    }
    product_response = client.post("/products", json=product_data)
    product_id = product_response.json()["id"]
    
    # Then, try to order more than available
    order_data = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 5
            }
        ]
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400  # Bad request due to insufficient stock
    assert "stock" in response.json()["detail"].lower()

def test_create_order_product_not_found(client):
    """Test creating an order with a non-existent product."""
    order_data = {
        "items": [
            {
                "product_id": 999,  # Non-existent product ID
                "quantity": 5
            }
        ]
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 404  # Not found 
