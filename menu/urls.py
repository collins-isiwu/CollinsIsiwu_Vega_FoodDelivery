from django.urls import path
from .views import (
    FoodListView,
    FoodDetailView,
    FoodCreateView,
    FoodDetailAdminView,
    FoodRatingCreateView,
    FoodCommentCreateView,
)

urlpatterns = [
    path('food/', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food_detail_for_users'),
    path('food/rate/', FoodRatingCreateView.as_view(), name='food_rate'), 
    path('food/comment/', FoodCommentCreateView.as_view(), name='food_comment'),
    # Admin-specific views
    path('admin/food/', FoodCreateView.as_view(), name='food_create'),  
    path('admin/food/<int:pk>/', FoodDetailAdminView.as_view(), name='food_detail_admin'),
]
