from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from menu.models import Food

CustomUser = get_user_model()

class MenuTestSetUp(APITestCase):
    def setUp(self):
        """
        Set up admin and non-admin users, as well as food items for testing.
        """
        # Create an admin user
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com', password='adminpass', is_admin=True)

        # Create a non-admin user
        self.normal_user = CustomUser.objects.create_user(
            email='user@example.com', password='userpass')

        self.admin_login_data = {"email": "admin@example.com", "password": "adminpass"}
        self.normal_login_data = {"email": "user@example.com", "password": "userpass"}

        # Sample food data
        self.food_data = {
            "name": "Ćevapi",
            "description": "Grilled minced meat sausages, typically served with flatbread.",
            "price": 12.50,
            "is_available": True
        }

        # Create a food item for update/delete tests
        self.food_item = Food.objects.create(
            name="Pljeskavica", description="Serbian-style grilled burger.", price=10.00, is_available=True
        )


        self.food_list_url = reverse('food_list')  
        self.food_create_url = reverse('food_create') 
        self.food_detail_url = reverse('food_detail_admin', kwargs={'pk': self.food_item.pk})  
        self.food_detail_user_url = reverse('food_detail_for_users', kwargs={'pk': self.food_item.pk}) 

class NonAdminFoodCreateTests(MenuTestSetUp):
    def test_non_admin_cannot_create_food(self):
        """
        Ensure a non-admin user cannot create a food item.
        """
        normal_login = self.client.post(reverse('login'), self.normal_login_data)
        normal_token = normal_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {normal_token}')

        response = self.client.post(self.food_create_url, self.food_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFoodDeleteTests(MenuTestSetUp):
    def test_admin_can_delete_food(self):
        """
        Ensure an admin user can delete a food item.
        """
        admin_login = self.client.post(reverse('login'), self.admin_login_data)
        admin_token = admin_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = self.client.delete(self.food_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

class UnauthenticatedUserTests(MenuTestSetUp):
    def test_unauthenticated_user_cannot_access(self):
        """
        Ensure unauthenticated users cannot access food-related functionality.
        """
        # Unauthenticated user tries to list food items
        response = self.client.get(self.food_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
     


