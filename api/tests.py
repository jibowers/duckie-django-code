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
        self.duckling_user.save()
	self.schedule = schedule('django.core.mail.send_mail',
             'Follow up',
             'This is in a test',
             'from@example.com',
             ['scout.julia@gmail.com'],
             schedule_type=Schedule.ONCE,
             next_run=timezone.now())

	self.duckling = Duckling(user=self.duckling_user, notification_schedule=self.schedule)

	message = "Positive vibe~~~"
	self.quack = Quack(message=message)


    def test_model_can_create_a_duckling(self):
        """Test the duckling model can create a duckling."""
        old_count = Duckling.objects.count()
        self.duckling.save()
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
	self.duckling.save()
	self.quack.save()
	old_count = self.duckling.quack_list.count()
	self.duckling.quack_list.add(self.quack)
	new_count = self.duckling.quack_list.count()
	self.assertNotEqual(old_count, new_count)

    def test_model_can_create_quack_with_submitted_by(self):
	""" Test that duckling can be added to Quack's submitted_by ForeignKey"""
	self.duckling.save()
	old_bool = self.quack.submitted_by
	self.quack.submitted_by = self.duckling
	self.quack.save()
	new_bool = self.quack.submitted_by
	self.assertNotEqual(old_bool, new_bool)

class ViewTestCase(TestCase):
    """Test suite for the api views"""
    
    def setUp(self):
	"""Define  the test client and other test variables"""
	user = User.objects.create(username="nerd")

	self.client = APIClient()
	self.quack_data = {'message': 'postive vibe ~~~', 'submitted_by': user.id}
	self.response = self.client.post(
	    reverse('createquack'),
	    self.quack_data,
	    format="json")

    def test_api_can_create_a_qauck(self):
	"""Test the api has quack creation capability."""
	self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

   
