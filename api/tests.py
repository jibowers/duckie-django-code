# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Duckling, Quack
from django.contrib.auth.models import User
from django_q.tasks import schedule
from django_q.models import Schedule
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
# Create your tests here.

class ModelTestCase(TestCase):
    """This class defines the test suite for the duckling model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.duckling_name = "Jimmy"
	self.duckling_password = "xyz"
	self.duckling_user = User(username=self.duckling_name, password=self.duckling_password)
#        self.duckling_user.save()
	
	#self.duckling = self.duckling_user.related_duckling
	message = "Positive vibe~~~"
	self.quack = Quack(message=message)


    def test_model_can_create_a_duckling(self):
        """Test the duckling model can create a duckling."""
        old_count = Duckling.objects.count()
        self.duckling_user.save()
        new_count = Duckling.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_quack(self):
	"""Test that the quack model can create a quack"""
	old_count = Quack.objects.count()
	self.quack.save()
	new_count = Quack.objects.count()
	self.assertNotEqual(old_count, new_count)

    def test_model_can_add_quack_to_duckling(self):
	"""Test that a quack can be added to a duckling's manyToManyField"""
	""" relies on the first two tests succeeding"""
	self.duckling_user.save()
	self.duckling = self.duckling_user.related_duckling

	self.quack.save()
	old_count = self.duckling.quack_list.count()
	self.duckling.quack_list.add(self.quack)
	new_count = self.duckling.quack_list.count()
	self.assertNotEqual(old_count, new_count)

    def test_model_can_create_quack_with_submitted_by(self):
	""" Test that duckling can be added to Quack's submitted_by ForeignKey"""
	self.duckling_user.save()
	old_bool = self.quack.submitted_by
	self.quack.submitted_by = self.duckling_user.related_duckling
	self.quack.save()
	new_bool = self.quack.submitted_by
	self.assertNotEqual(old_bool, new_bool)

class ViewTestCase(TestCase):
    """Test suite for the api views"""
    
    def setUp(self):
	"""Define  the test client and other test variables"""
	#user = User.objects.create(username="nerd")

	self.duckling_name = "Jimmy"
        self.duckling_password = "xyz"
        self.duckling_user = User(username=self.duckling_name, password=self.duckling_password)
        self.duckling_user.save()
        
        self.duckling = self.duckling_user.related_duckling

	self.client = APIClient()
	self.client.force_authenticate(user=self.duckling.user)
	
	self.quack_data = {'message': 'postive vibe ~~~', 'submitted_by': self.duckling.id}
	self.response = self.client.post(
	    reverse('createquack'),
	    self.quack_data,
	    format="json")

    def test_api_can_create_a_qauck(self):
	"""Test the api has quack creation capability."""
	self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_retrieve_empty_quack_list(self):
        """Test the api has quack retrieval capability, even if quack list is empty"""
        response = self.client.get(
            '/retrievequacks/10/', #must have 10 in there bc url requires number
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_retieve_quack_list(self):
	"""Test the api has quack retieval capability."""
	quack = Quack(message="positive vibe~")
	quack.save()
	self.duckling.quack_list.add(quack)   
	response = self.client.get(
            '/retrievequacks/10/',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_register_user(self):
	"""Test the api has user creation capability"""
	username = "nerd"
	password = "yaypassword"
	self.user_data = {'username':username, 'password':password}
	response = self.client.post(
            reverse('registeruser'),
            self.user_data,
            format="json")
	self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#test_api_can_create_duckling not needed because registering a user a
#automatically creates Duckling (with default vals), using signal

    def test_api_can_get_settings(self):
	"""Test the api can get a duckling's settings"""
	
	response = self.client.get(
	    '/getupdateduckling/',
	    format="json"
	)
	self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_api_can_update_settings(self):
	"""Test the api can update a duckling's settings"""
	put_info = {"wants_push": False, "minute_frequency": 1456, "preferred_time": ""}
	response = self.client.put(
	    reverse('update'),
	    put_info,
	    format = "json"
	)
	
	self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_sync_to_newer_quack(self):
	response = self.client.get(
	    '/synctonewer/',
	    format="json"
	)
	self.assertEqual(response.status_code, status.HTTP_200_OK)

