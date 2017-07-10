# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics, permissions
from .serializers import QuackSerializer
from .models import Quack, Duckling
from rest_framework.response import Response

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
