from django.urls import path
from api.views import ProductListView, ProductCreateView, OrderCreateView

urlpatterns = [
    path('products', ProductListView.as_view(), name='list_products'),
    path('products/create', ProductCreateView.as_view(), name='create_product'),
    path('orders', OrderCreateView.as_view(), name='create_order'),
]
