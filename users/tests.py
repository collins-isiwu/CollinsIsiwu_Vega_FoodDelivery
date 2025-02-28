from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP

CustomUser = get_user_model()

class UserTestsSetUp(APITestCase):
    def setUp(self):
        """
        Create test user data to use across all test cases.
        """
        self.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        self.admin_data = {
            "email": "adminuser@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "password": "password123",
            "is_admin": True
        }
        self.login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        self.logout_data = {
            "refresh_token": ""
        }


class UserRegistrationViewTests(UserTestsSetUp):
    def test_user_registration(self):
        """
        Ensure that a user can register successfully.
        """
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], "User registered successfully.")


class AdminRegistrationViewTests(UserTestsSetUp):
    def test_admin_registration(self):
        """
        Ensure that an admin user can register successfully.
        """
        response = self.client.post(reverse('register_admin'), self.admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], "Admin user registered successfully.")


class UserLoginViewTests(UserTestsSetUp):
    def test_user_login(self):
        """
        Ensure that a user can log in and receive a valid JWT token.
        """
        self.client.post(reverse('register'), self.user_data)
        response = self.client.post(reverse('login'), self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data'])


class PasswordResetRequestViewTests(UserTestsSetUp):
    def test_password_reset_request(self):
        """
        Ensure that the password reset request sends an OTP.
        """
        self.client.post(reverse('register'), self.user_data) 
        response = self.client.post(reverse('password_reset_request'), {"email": self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], "Use OTP from this response to Verify Password Reset.")


class PasswordResetViewTests(UserTestsSetUp):
    def test_password_reset(self):
        """
        Ensure that a user can reset the password using OTP.
        """
        self.client.post(reverse('register'), self.user_data)
        response = self.client.post(reverse('password_reset_request'), {"email": self.user_data['email']})

        otp_entry = PasswordResetOTP.objects.get(user__email=self.user_data['email'])
        otp = otp_entry.otp 

        reset_data = {
            "email": self.user_data['email'],
            "otp": otp,
            "new_password": "newpassword123"
        }
        reset_response = self.client.post(reverse('password_reset_verify'), reset_data)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)
        self.assertTrue(reset_response.data['success'])
        self.assertEqual(reset_response.data['message'], "Password reset successful.")



