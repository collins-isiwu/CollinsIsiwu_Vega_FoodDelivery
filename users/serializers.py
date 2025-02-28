from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import PasswordReset


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering regular users.
    Handles validation of input data and user creation with the necessary fields.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class AdminCreationSerializer(UserRegistrationSerializer):
    """
    Serializer for registering admin users.
    Extends the regular user registration but enforces the 'is_admin' flag.
    """
    class Meta(UserRegistrationSerializer.Meta):
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.is_admin = True
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login.
    Validates user credentials (email and password) and returns authentication tokens.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for handling user logout by blacklisting the refresh token.
    """
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        """
        Validate that the refresh token is provided in the request data.
        """
        self.token = attrs.get('refresh_token')
        if not self.token:
            raise ValidationError('No refresh token provided.')
        return attrs
    
    def save(self, **kwargs):
        """
        Blacklist the provided refresh token to invalidate it for future use.
        """
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError('Token is invalid or expired!')


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer to handle password reset requests and OTP generation.
    """
    email = serializers.EmailField()

    def create_otp(self, user):
        """
        Create or update an OTP for the user.
        """
        otp_entry, created = PasswordReset.objects.update_or_create(user=user)
        if not created:
            otp_entry.timestamp = timezone.now()
            otp_entry.save() 
        otp_entry.generate_otp()
        return otp_entry

    def send_otp_email(self, otp, email):
        """
        Send OTP to the user's email.
        """
        send_mail(
            'Password Reset OTP',
            f'Your OTP for resetting your password is: {otp}',
            'no-reply@fooddelivery.com',
            [email],
            fail_silently=False,
        )

    def save(self):
        """
        Generate OTP, associate it with the user, and send it via email after validating the email.
        """
        email = self.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")

        # Generate OTP and send email
        otp_entry = self.create_otp(user)
        self.send_otp_email(otp_entry.otp, user.email)

        return {'email': email, 'OTP': otp_entry.otp}


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer to reset the password using the OTP.
    """
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the OTP and its expiration.
        """
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")
        
        try:
            otp_entry = PasswordReset.objects.get(user=user, otp=data['otp'])
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or token.")

        if timezone.now() > otp_entry.timestamp + timedelta(minutes=10):
            raise serializers.ValidationError("OTP has expired.")

        data['user'] = user
        
        return data

    def save(self):
        """
        Reset the user's password after OTP verification.
        """
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
