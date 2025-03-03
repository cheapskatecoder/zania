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


## Database Configuration

The application uses PostgreSQL as its database. The following environment variables can be configured:

- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_DB`: Database name (default: ecommerce)
- `POSTGRES_HOST`: Database host (default: db)
- `POSTGRES_PORT`: Database port (default: 5432)

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


### Local Development with Docker
1. Build the container using docker-compose. The server is set to autoreload everytime you change any of the files.

```
# to build the container from scratch
docker-compose up --build

# if the container has already been built
docker-compose up
```

## Testing

Run the tests using pytest:

```
# if you're using the project without docker and local dependencies such as database connections already setup.
pytest


# if you're using docker
docker run -it <container-name> pytest
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
