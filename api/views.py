# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import datetime

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

#I don't need this anymore with UpdateSettingsView also providing quacks
#However this might be useful if modified to get a certain number of quacks
# maybe as www.ec2....com/quacks/(number)
class RetrieveQuackView(generics.ListAPIView):
    queryset = Quack.objects.all()
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, number):
	number = int(number)
	queryset = self.request.user.related_duckling.quack_list.order_by('-submit_date')[:number]
	serializer = QuackSerializer(queryset, many=True)
	return Response(serializer.data)

class ListDucklingsView(generics.ListAPIView):
    queryset = Duckling.objects.all()
    serializer_class=DucklingSerializer

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UpdateSettingsView(generics.RetrieveUpdateAPIView):
#    queryset = Duckling.objects.all()
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

class SyncToNewerQuackView(generics.ListAPIView):
    ## get ten most recently approved quacks
    ## if < 10 approved quacks, take all of them (is done automatically)
    ## if filter ten to only take ones that are newer than latest quack of quack_list (to avoid duplicates... which is done automatically)

    # GET view
    queryset = Quack.objects.order_by('-submit_date')[:10]
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
	my_quack_list = self.request.user.related_duckling.quack_list
	try:
		previous_date = my_quack_list.order_by('-submit_date')[0].submit_date
		queryset = Quack.objects.filter(is_approved =True).filter(submit_date__gt=previous_date).order_by('-submit_date')[:10]
	except IndexError:
		queryset = Quack.objects.filter(is_approved=True).order_by('-submit_date')[:10]

	for q in queryset:
		self.request.user.related_duckling.quack_list.add(q)
        serializer = QuackSerializer(queryset, many=True)
        return Response(serializer.data)

class ModeratorListView(generics.ListAPIView):
    queryset = Quack.objects.filter(has_been_processed=False).order_by('submit_date')
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated, IsModerator,)

    def list(self, request, number):
        number = int(number)
        queryset = Quack.objects.filter(has_been_processed=False).order_by('submit_date')[:number]
        serializer = QuackSerializer(queryset, many=True)
        return Response(serializer.data)

class ModeratorUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Quack.objects.all()
    serializer_class = QuackSerializer
    permission_classes = (permissions.IsAuthenticated, IsModerator,)

    def perform_update(self, serializer):
	## set has_been_processed to True and is_approved to True or False
	## set submit_date to the current time
	## possibly delete rejected quack
	this_quack = Quack.objects.get(pk=self.kwargs['pk'])
	this_quack.has_been_processed = True
	this_quack.is_approved = serializer.validated_data['is_approved']
	this_quack.submit_date = datetime.datetime.now()
	this_quack.save()
