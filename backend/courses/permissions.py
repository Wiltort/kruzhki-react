from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only admins
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
    

class IsAdminOrAllowedTeacherOrReadOnly(permissions.BasePermission):
    """
    Permission to teacher of group to readonly and admin to edit
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return user.is_superuser or obj.teacher == user


class IsAdminOrTeacher(permissions.BasePermission):
 
     def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff
        