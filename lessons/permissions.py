from rest_framework import permissions

class IsManagerUser(permissions.BasePermission):
    """
    Разрешение только для менеджеров.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return bool(request.user and request.user.is_authenticated and request.user.role == 'manager') 