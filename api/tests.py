from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Product, Order


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_products_empty(self):
        """
        Ensure listing products returns an empty list initially.
        """
        url = reverse("list_products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        url = reverse("create_product")
        data = {
            "name": "Laptop",
            "description": "A powerful laptop",
            "price": 999.99,
            "stock": 10,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="Laptop").exists())
        product = Product.objects.get(name="Laptop")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.stock, 10)


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_order_insufficient_stock(self):
        """
        Create a product with limited stock, then try to order more than available.
        """
        product = Product.objects.create(
            name="Phone", description="A smartphone", price=500.00, stock=1
        )

        url = reverse("create_order")
        data = {"items": [{"product": product.id, "quantity": 2}]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock for product 'Phone'", str(response.json()))

    def test_create_order_successful(self):
        """
        Create multiple products, place a valid order, and verify results.
        """
        product1 = Product.objects.create(
            name="Phone", description="Smartphone", price=500.00, stock=10
        )
        product2 = Product.objects.create(
            name="Headphones", description="Wireless", price=150.00, stock=5
        )

        url = reverse("create_order")
        data = {
            "items": [
                {"product": product1.id, "quantity": 2},
                {"product": product2.id, "quantity": 1},
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertIn("id", response_data)
        self.assertEqual(response_data["status"], "pending")
        self.assertEqual(response_data["total_price"], 1150.00)  # 500*2 + 150*1

        order_id = response_data["id"]
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.total_price, 1150.00)
        self.assertEqual(order.items.count(), 2)

        # Check stock deduction
        product1.refresh_from_db()
        product2.refresh_from_db()
        self.assertEqual(product1.stock, 8)  # 10 - 2
        self.assertEqual(product2.stock, 4)  # 5 - 1
