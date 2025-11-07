from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and (request.user.is_superuser or getattr(request.user, "role", None) in ("admin", "support")):
            return True
        owner = getattr(obj, "customer", None) or getattr(obj, "author", None)
        return owner == request.user

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

