from rest_framework.permissions import BasePermission
from .models import Duckling

class IsModerator(BasePermission):
    """Custom permission class to allow only moderators to edit quacks"""
    #change serializer read_only_fields to not include allowed/rejected
    def has_object_permission(self,request, view, obj):
         return request.user.related_duckling.is_moderator

class IsOwner(BasePermission):
    """Custom permission class to allow only the related user of a duckling to update themselves"""
    def has_object_permission(self, request, view, obj):
	"""Return true if permission is granted to the bucketlist owner."""
        if isinstance(obj, Duckling):
             return obj.user == request.user
        return obj.user == request.user

