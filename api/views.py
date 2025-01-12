from rest_framework import generics
from api.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer

class ProductListView(generics.ListAPIView):
    """
    GET /products -> list products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    """
    POST /products/create -> create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(generics.CreateAPIView):
    """
    POST /orders -> create a new order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
