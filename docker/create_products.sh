#!/usr/bin/env bash

# Base URL for the API
BASE_URL="http://localhost:8000/api"

# 1. Create multiple products
echo "Creating Products..."
curl -X POST "$BASE_URL/products" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Laptop",
           "description": "Powerful laptop with 16GB RAM",
           "price": 999.99,
           "stock": 10
         }'
echo -e "\n---"

curl -X POST "$BASE_URL/products" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Headphones",
           "description": "Wireless and noise-canceling",
           "price": 199.99,
           "stock": 20
         }'
echo -e "\n---"

curl -X POST "$BASE_URL/products" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Wireless Mouse",
           "description": "Ergonomic design",
           "price": 29.99,
           "stock": 50
         }'
echo -e "\n---"

curl -X POST "$BASE_URL/products" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Keyboard",
           "description": "Mechanical with RGB backlight",
           "price": 89.99,
           "stock": 30
         }'
echo -e "\n---"

curl -X POST "$BASE_URL/products" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Monitor",
           "description": "24-inch FHD",
           "price": 149.99,
           "stock": 15
         }'
echo -e "\n---"

# 2. (Optional) List products to confirm
echo -e "\nListing all products to confirm IDs and details..."
curl -X GET "$BASE_URL/products"
echo -e "\n---"

# 3. Create an order
#    NOTE: You'll need to reference the actual product IDs returned above. 
#    Here, we assume the first 5 product IDs are 1, 2, 3, 4, 5 for demonstration.
echo -e "\nPlacing an Order..."
curl -X POST "$BASE_URL/orders" \
     -H "Content-Type: application/json" \
     -d '{
           "items": [
             { "product": 1, "quantity": 2 },
             { "product": 2, "quantity": 1 },
             { "product": 3, "quantity": 5 }
           ]
         }'
echo -e "\n---"

# 4. Done
echo "Data population complete!"
