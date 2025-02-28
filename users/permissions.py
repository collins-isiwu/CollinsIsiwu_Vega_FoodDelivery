from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission class that allows access only to admin users.
    """
    def has_permission(self, request, view):
        """
        Return True if the user is authenticated and is an admin.
        """
        return request.user and request.user.is_authenticated and request.user.is_admin
