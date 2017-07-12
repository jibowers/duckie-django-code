# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, permissions
from .serializers import QuackSerializer, DucklingSerializer, UserSerializer
from .models import Quack, Duckling
from rest_framework.response import Response
from .tasks import update_or_add_schedule
from .permissions import IsModerator, IsOwner
from django.contrib.auth.models import User

# Create your views here.

class CreateQuackView(generics.CreateAPIView): 
    """This class defines the create quack behavior of our rest api"""
    queryset = Quack.objects.all()
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
	"""Save the post data when creating a new quack object"""
	serializer.save(submitted_by=self.request.user.related_duckling)

class RetrieveQuackView(generics.ListAPIView):
    queryset = Quack.objects.all()
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
	queryset = self.request.user.related_duckling.quack_list
	serializer = QuackSerializer(queryset, many=True)
	return Response(serializer.data)

class ListDucklingsView(generics.ListAPIView):
    queryset = Duckling.objects.all()
    serializer_class=DucklingSerializer

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UpdateSettingsView(generics.RetrieveUpdateAPIView):
    queryset = Duckling.objects.all()
    serializer_class = DucklingSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    partial = True   
 
    def get_object(self):
        queryset = self.request.user.related_duckling
    
    def retrieve(self, request):
	queryset = self.request.user.related_duckling
	serializer = DucklingSerializer(queryset)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
#        serializer.save(user=Duckling.objects.get(user=self.request.user).user)	
## update duckling's notification_schedule, or create if already exists
	#super(serializer).perform_update
	this_duckling = self.request.user.related_duckling
	min = serializer.validated_data['minute_frequency']
	pref_time = serializer.validated_data['preferred_time']
	this_duckling.minute_frequency = min
	this_duckling.preferred_time= pref_time
	this_duckling.wants_push = serializer.validated_data['wants_push']
	this_duckling.save()
	update_or_add_schedule(self.request.user.related_duckling)        
