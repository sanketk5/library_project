from rest_framework import permissions

class CheckMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'LIBRARIAN'

class CheckLibrarian(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'LIBRARIAN':
            return True
        return True