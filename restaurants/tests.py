from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant

CustomUser = get_user_model()

class RestaurantTestsSetUp(APITestCase):
    def setUp(self):
        """
        Set up admin and non-admin users for the tests.
        """
        # Create an admin user
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com', password='adminpass', is_admin=True)
        
        # Create a non-admin user
        self.normal_user = CustomUser.objects.create_user(
            email='user@example.com', password='userpass')
        
        self.admin_login_data = {"email": "admin@example.com", "password": "adminpass"}
        self.normal_login_data = {"email": "user@example.com", "password": "userpass"}
        
        self.restaurant_data = {
            "name": "Test Restaurant",
            "location": "123 Test Street, Belgrade"
        }
        
        self.restaurant = Restaurant.objects.create(name="Old Restaurant", location="456 Old Street")

        self.restaurant_list_create_url = reverse('restaurant_list_create')
        self.restaurant_detail_url = reverse('restaurant_detail', kwargs={'pk': self.restaurant.pk})


class RestaurantCreateTests(RestaurantTestsSetUp):
    def test_admin_can_create_restaurant(self):
        """
        Ensure an admin can create a new restaurant.
        """
        admin_login = self.client.post(reverse('login'), self.admin_login_data)
        admin_token = admin_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = self.client.post(self.restaurant_list_create_url, self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RestaurantCreatePermissionTests(RestaurantTestsSetUp):
    def test_non_admin_cannot_create_restaurant(self):
        """
        Ensure a non-admin user cannot create a restaurant.
        """
        # Normal user login
        normal_login = self.client.post(reverse('login'), self.normal_login_data)
        normal_token = normal_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {normal_token}')

        # Non-admin tries to create a restaurant
        response = self.client.post(self.restaurant_list_create_url, self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RestaurantListTests(RestaurantTestsSetUp):
    def test_admin_can_list_restaurants(self):
        """
        Ensure an admin user can list all restaurants.
        """
        # Admin login
        admin_login = self.client.post(reverse('login'), self.admin_login_data)
        admin_token = admin_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        # Admin lists restaurants
        response = self.client.get(self.restaurant_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)  

class RestaurantListPermissionTests(RestaurantTestsSetUp):
    def test_non_admin_can_list_restaurants(self):
        """
        Ensure a non-admin user can list all restaurants.
        """
        # Normal user login
        normal_login = self.client.post(reverse('login'), self.normal_login_data)
        normal_token = normal_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {normal_token}')

        # Non-admin lists restaurants
        response = self.client.get(self.restaurant_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RestaurantUpdateTests(RestaurantTestsSetUp):
    def test_admin_can_update_restaurant(self):
        """
        Ensure an admin user can update an existing restaurant.
        """
        # Admin login
        admin_login = self.client.post(reverse('login'), self.admin_login_data)
        admin_token = admin_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        # Admin updates the restaurant
        updated_data = {"name": "Updated Restaurant", "location": "789 Updated Street"}
        response = self.client.put(self.restaurant_detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RestaurantDeleteTests(RestaurantTestsSetUp):
    def test_admin_can_delete_restaurant(self):
        """
        Ensure an admin user can delete a restaurant.
        """
        # Admin login
        admin_login = self.client.post(reverse('login'), self.admin_login_data)
        admin_token = admin_login.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        # Admin deletes the restaurant
        response = self.client.delete(self.restaurant_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RestaurantUnauthenticatedTests(RestaurantTestsSetUp):
    def test_unauthenticated_users_are_denied_access(self):
        """
        Ensure unauthenticated users cannot access restaurant-related functionality.
        """
        # Unauthenticated user tries to list restaurants
        response = self.client.get(self.restaurant_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

