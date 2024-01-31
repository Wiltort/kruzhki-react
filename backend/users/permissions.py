from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == "POST":
            return not(user.is_authenticated) or user.is_superuser
        return user.is_superuser or user == obj