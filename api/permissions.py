from rest_framework.permissions import BasePermission
from .models import Bucketlist

class IsModerator(BasePermission):
    """Custom permission class to allow only moderators to edit quacks"""
    #change serializer read_only_fields to not include allowed/rejected
    def has_object_permission(self,request, view, obj):
         return request.user.related_duckling.is_moderator
