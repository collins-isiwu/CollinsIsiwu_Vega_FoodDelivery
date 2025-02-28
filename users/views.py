from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, UserLoginSerializer, LogoutSerializer, AdminCreationSerializer, PasswordResetRequestSerializer, PasswordResetSerializer

class UserRegistrationView(APIView):
    """
    API view for user registration.
    Accepts user data (email, first_name, last_name, password) and creates a new user.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle the POST request for user registration.
        Validates and creates a new user, and returns a response with a success status.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'User registered successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'User registration failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    """
    API view for admin registration.
    Accepts admin data (email, first_name, last_name, password) and creates an admin user.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle the POST request for admin registration.
        Validates and creates a new admin user, and returns a response with a success status.
        """
        serializer = AdminCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'error': None,
                'message': 'Admin user registered successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Admin registration failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    """
    API view for user login.
    Authenticates a user with their email and password and returns JWT tokens on success.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle the POST request for user login.
        Authenticates the user, issues JWT tokens, and returns a success response.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'error': None,
                    'message': 'Login successful.',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'error': 'Invalid credentials',
                'message': 'Authentication failed.',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Invalid input.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetRequestView(APIView):
    """
    API view for requesting a password reset (sends OTP to the user's email).
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle POST request for password reset. Validate email, generate OTP, and send it via email.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'error': None,
                'message': 'Use OTP from this response to Verify Password Reset.',
                'data': data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Password reset request failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """
    API view for verifying the OTP and resetting the password.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle POST request to verify OTP and reset the user's password.
        """
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'error': None,
                'message': 'Password reset successful.',
                'data': None
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Password reset failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API view to handle user logout by blacklisting the refresh token.
    """
    def post(self, request):
        """
        Handle POST request to blacklist the user's refresh token.
        """
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_205_RESET_CONTENT,
                'error': None,
                'message': 'Logout successful.',
                'data': None
            }, status=status.HTTP_205_RESET_CONTENT)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors,
            'message': 'Logout failed.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)