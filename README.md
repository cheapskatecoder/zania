# E-Commerce RESTful API

A production-grade RESTful API for a simple e-commerce platform built with FastAPI and SQLite.

## Features

- **Product Management**: View and add products
- **Order Processing**: Place orders with stock validation
- **Data Validation**: Comprehensive validation with Pydantic
- **Error Handling**: Graceful error handling with appropriate HTTP status codes
- **Testing**: Comprehensive test suite

## API Endpoints

- `GET /products`: Retrieve all available products
- `POST /products`: Add a new product
- `POST /orders`: Place an order with stock validation

## Getting Started

### Prerequisites

- Docker
- Python 3.9+ (for local development)

### Running with Docker

1. Build the Docker image:
```
docker build -t ecommerce-api .
```

2. Run the container:
```
docker run -p 8000:8000 ecommerce-api
```

3. Access the API at `http://localhost:8000`

### Local Development

1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
uvicorn app.main:app --reload
```

4. Access the API at `http://localhost:8000`

## Testing

Run the tests using pytest:

```
pytest
```

## API Documentation

FastAPI provides automatic API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Data Models

### Product
- **id**: Unique identifier (integer)
- **name**: Product name (string)
- **description**: Product description (string)
- **price**: Product price (float)
- **stock**: Available quantity (integer)

### Order
- **id**: Unique identifier (integer)
- **products**: List of products with quantities
- **total_price**: Total order price (float)
- **status**: Order status ("pending" or "completed")

## Example Requests

### Creating a Product
```bash
curl -X 'POST' \
  'http://localhost:8000/products' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Smartphone",
  "description": "Latest model smartphone",
  "price": 699.99,
  "stock": 50
}'
```

### Placing an Order
```bash
curl -X 'POST' \
  'http://localhost:8000/orders' \
  -H 'Content-Type: application/json' \
  -d '{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}'
```

## Database Configuration

The application uses PostgreSQL as its database. The following environment variables can be configured:

- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_DB`: Database name (default: ecommerce)
- `POSTGRES_HOST`: Database host (default: db)
- `POSTGRES_PORT`: Database port (default: 5432)

## Running with Docker Compose

1. Start the services:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

## Local Development

1. Install PostgreSQL on your system
2. Create a database named 'ecommerce'
3. Set up environment variables or update database.py with your PostgreSQL credentials
4. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## Running Tests

The tests use a separate PostgreSQL database. Make sure the test database exists before running tests:

```bash
docker-compose up test_db -d
pytest
``` 