# E-commerce API (Django + DRF)

Welcome to the **E-commerce API**, built with **Django** and the **Django REST Framework** (DRF). This project provides basic functionality for managing products and orders, making it a foundation for a more comprehensive e-commerce platform.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation & Setup](#installation--setup)
3. [Database Migrations](#database-migrations)
4. [Running the Server](#running-the-server)
5. [API Endpoints](#api-endpoints)
6. [Postman Collection](#postman-collection)
7. [Running Tests](#running-tests)
8. [Possible Improvements](#possible-improvements)

---

## Project Structure

The project structure is organized as follows:


```bash
.
├── README.md
├── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docker
│   ├── Dockerfile
│   ├── create_products.sh
│   └── start_server_setup_dummy_data.sh
├── manage.py
├── requirements.txt
└── zania
    ├── __init__.py
    ├── asgi.py
    ├── settings
    │   ├── base.py
    │   ├── dev.py
    │   └── prod.py
    ├── urls.py
    └── wsgi.py

```

Key components:
- **`api/models.py`**: Defines `Product`, `Order`, and `OrderItem` models.
- **`api/serializers.py`**: DRF serializers for data validation and transformation.
- **`api/views.py`**: Class-based views for listing/creating `Products` and creating `Orders`.
- **`api/urls.py`**: URL configurations specific to the API endpoints.
- **`api/tests.py`**: Django test cases for the API.
- **`docker/`**: Contains scripts for Docker automation and populating data.
- **`requirements.txt`**: Lists project dependencies.

---

## Installation & Setup

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/your-username/ecommerce-api.git
   cd ecommerce-api
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Database Migrations

Run the following to create the database schema:

```bash
python manage.py migrate
```

This will set up tables for `Product`, `Order`, and `OrderItem`.

---

## Running the Server

Start the Django development server with:

```bash
python manage.py runserver
```

Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

### 1. **GET `/api/products`**
**Description**: Retrieve a list of all products.  
**Example Request**:
```bash
curl -X GET http://127.0.0.1:8000/api/products
```
**Response**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "A powerful laptop",
    "price": 999.99,
    "stock": 10
  },
  {
    "id": 2,
    "name": "Headphones",
    "description": "Wireless and noise-cancelling",
    "price": 199.99,
    "stock": 20
  }
]
```

---

### 2. **POST `/api/products/create`**
**Description**: Add a new product to the database.  
**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/products/create \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Laptop",
           "description": "Powerful laptop with 16GB RAM",
           "price": 999.99,
           "stock": 10
         }'
```
**Response**:
```json
{
  "id": 3,
  "name": "Laptop",
  "description": "Powerful laptop with 16GB RAM",
  "price": 999.99,
  "stock": 10
}
```

---

### 3. **POST `/api/orders`**
**Description**: Place an order for products.  
**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/orders \
     -H "Content-Type: application/json" \
     -d '{
           "items": [
             { "product": 1, "quantity": 2 },
             { "product": 2, "quantity": 1 }
           ]
         }'
```
**Response**:
```json
{
  "id": 1,
  "total_price": 1399.97,
  "status": "pending"
}
```

---

## Postman Collection

To simplify testing, a **Postman collection** is included in the repository.  

1. **Locate the collection**: `ecommerce.postman_collection.json`.
2. **Import it into Postman**:
   - Open Postman.
   - Click **Import** and select the JSON file.
3. **Set variables**:
   - Update the `base_url` variable in the collection (e.g., `http://127.0.0.1:8000/api`).

---

## Running Tests

Run tests with Django’s built-in test framework:

```bash
python manage.py test
```

This runs all test cases defined in `api/tests.py`.

---

## Possible Improvements

This is a basic implementation of an e-commerce API. Here’s a list of enhancements to consider:

### 1. **Authentication & Authorization**
   - Add user authentication (e.g., token-based or session-based).
   - Restrict product creation to admin users.
   - Allow customers to view only their own orders.

### 2. **Pagination**
   - Implement pagination for the `/products` endpoint to handle large datasets.

### 3. **Filtering & Sorting**
   - Allow filtering products by price, name, or stock levels.
   - Enable sorting options for `/products` (e.g., by price or name).

### 4. **Enhanced Order Management**
   - Add order statuses beyond "pending" and "completed" (e.g., "shipped", "cancelled").
   - Include customer information in orders.

### 5. **Improved Stock Management**
   - Add stock alerts when inventory levels are low.
   - Implement a "restock" endpoint for admins.

### 6. **Error Handling**
   - Provide more detailed error messages.
   - Validate order items (e.g., prevent duplicates).

### 7. **Unit Tests**
   - Add more comprehensive test cases for edge cases and failure scenarios.

### 8. **Deployment Optimization**
   - Use Gunicorn or uWSGI with Nginx for production.
   - Add Docker support (build and run the app as a container).

### 9. **Database Optimization**
   - Use indexing for frequently queried fields (e.g., `price` or `name` in `Product`).
   - Add caching for `/products` to improve response time.

---

## Conclusion

This project demonstrates a simple e-commerce backend built with Django and DRF. While functional, there’s ample room for improvement to make it production-ready. Feel free to extend it and adapt it to your specific needs.  
```