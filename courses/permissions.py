from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ на чтение всем пользователям,
    а на изменение только менеджерам.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return request.user.is_staff 