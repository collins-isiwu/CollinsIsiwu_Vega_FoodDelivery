from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

CustomUser = get_user_model()

class EmailBackend(ModelBackend):
    """
    Authenticate using email address
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user  
        return None 