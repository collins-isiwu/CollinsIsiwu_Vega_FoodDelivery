from django.urls import path
from .views import OrderCreateView, OrderDetailView, OrderListView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='create_order'),  
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'), 
    path('orders', OrderListView.as_view(), name='list_orders'), 
]
