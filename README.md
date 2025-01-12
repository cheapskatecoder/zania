# E-commerce API (Django + DRF)

Welcome to the **E-commerce API**, built with **Django** and the **Django REST Framework** (DRF). This project provides functionality for managing products and orders, making it a foundational backend for an e-commerce platform.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation & Setup](#installation--setup)
3. [Database Migrations](#database-migrations)
4. [Running the Server](#running-the-server)
5. [Deployment](#deployment)
6. [API Endpoints](#api-endpoints)
7. [Postman Collection](#postman-collection)
8. [Running Tests](#running-tests)
9. [Possible Improvements](#possible-improvements)

---

## Project Structure

Below is the relevant project structure:

```bash
.
├── README.md
├── api
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
├── docker
│   ├── Dockerfile
│   ├── create_products.sh
│   └── start_server_setup_dummy_data.sh
├── manage.py
├── requirements.txt
└── zania
    ├── settings/
    │   ├── base.py
    │   ├── dev.py
    │   └── prod.py
    ├── urls.py
    └── wsgi.py
```

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

Run the following to set up the database schema:

```bash
python manage.py migrate
```

> **Note**:  
> The `dev.py` settings file is configured to use **SQLite3** by default, ensuring the development environment works out of the box without requiring PostgreSQL. For production, refer to `prod.py`, which is configured to use PostgreSQL.

---

## Running the Server

Start the Django development server with:

```bash
python manage.py runserver
```

Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Deployment

To deploy the project in a production environment, follow these steps:

### 1. Build the Docker Image

```bash
docker build -t ecommerce-api .
```

### 2. Run the Container

For a **production** setup, use the following command to run the container. It uses the `prod.py` settings:

```bash
docker run -p 8000:8000 -e DJANGO_SETTINGS_MODULE=zania.settings.prod ecommerce-api
```

### 3. Additional Steps for Production
- Use a proper WSGI server like **Gunicorn**:
  ```bash
  gunicorn zania.wsgi:application --bind 0.0.0.0:8000
  ```
- Deploy behind a reverse proxy like **Nginx** for better performance and security.
- Set up **PostgreSQL** as the database by configuring the `prod.py` settings file.

---

## API Endpoints

### 1. **GET `/api/products`**
Retrieve a list of all products.
```bash
curl -X GET http://127.0.0.1:8000/api/products
```

### 2. **POST `/api/products/create`**
Add a new product.
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

### 3. **POST `/api/orders`**
Place an order.
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

To run the tests:

```bash
python manage.py test
```

---

## Possible Improvements

This project is a basic implementation. Here are some areas for improvement:

1. **Authentication & Authorization**:
   - Add user authentication (e.g., token-based or session-based).
   - Restrict product creation to admin users.
   - Allow customers to view only their own orders.

2. **Improved Error Handling**:
   - Return more descriptive error messages.
   - Validate order payloads more comprehensively.

3. **Enhanced Order Management**:
   - Add additional order statuses (e.g., "shipped", "cancelled").
   - Include customer information in orders.

4. **Database Optimization**:
   - Use PostgreSQL in production for better performance.
   - Add indexes on frequently queried fields (e.g., `price` in `Product`).

5. **Pagination, Filtering, and Sorting**:
   - Implement pagination for `/products`.
   - Add filtering and sorting options (e.g., by price, stock).

6. **Deployment**:
   - Set up a CI/CD pipeline for automated builds and deployment.
   - Use environment variables for sensitive settings (e.g., database credentials).

7. **Tests**:
   - Expand test coverage to include edge cases and negative scenarios.

---

This project serves as a foundation for building a more comprehensive e-commerce system. Contributions and feedback are welcome!