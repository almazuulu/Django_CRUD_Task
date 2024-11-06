from rest_framework import permissions


class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    Allow to read for any users, 
    but for the adjustments authentication is needed
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
