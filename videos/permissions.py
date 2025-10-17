from rest_framework.permissions import BasePermission, SAFE_METHODS
from subscriptions.utils import has_active_subscription

class CanViewOrEditVideo(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated and request.user.is_staff)

        if obj.is_free:
            return True
        return has_active_subscription(request.user)
