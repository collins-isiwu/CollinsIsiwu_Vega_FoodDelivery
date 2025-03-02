from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/account/', include('users.urls')),
    path('api/v1/restaurants/', include('restaurants.urls')),
    path('api/v1/menus/', include('menu.urls')),
    path('api/v1/order/', include('order.urls')),
]
