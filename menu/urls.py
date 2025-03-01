from django.urls import path
from .views import (
    FoodListView,
    FoodDetailForUsersView,
    FoodCreateView,
    FoodDetailView,
)

urlpatterns = [
    path('food/', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>/', FoodDetailForUsersView.as_view(), name='food_detail_for_users'),
    # Admin-specific views
    path('admin/food/', FoodCreateView.as_view(), name='food_create'),  
    path('admin/food/<int:pk>/', FoodDetailView.as_view(), name='food_detail_admin'),
]
