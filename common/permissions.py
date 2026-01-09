from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import timezone, timedelta
from django.utils import timezone


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    

class CanEditWithin15Minutes(BasePermission):
    def  has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=15)
    

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method in ['GET','PUT','PATCH','DELETE']:
            return True
        return False

class IsCustomAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff