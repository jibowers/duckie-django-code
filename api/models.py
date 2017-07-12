# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.models import Schedule

# Create your models here.

class Duckling(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE, related_name='related_duckling')
    is_moderator = models.BooleanField(default=False)
    wants_push = models.BooleanField(default=False)
    notification_schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    quack_list = models.ManyToManyField('Quack', blank=True)
    minute_frequency = models.IntegerField(default = 1440)
    preferred_time = models.CharField(max_length=4, default = "", blank=True)

    def __str__(self):
        """return a human readable representation of the model instance"""
        return "{}".format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Duckling.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.related_duckling.save()

class Quack(models.Model):
    message = models.CharField(max_length=500)
    submitted_by = models.ForeignKey(Duckling, null=True, on_delete=models.SET_NULL)
    submit_date = models.DateTimeField(auto_now_add=True)
    has_been_processed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        """return a human readabel represenation of the model instance"""
        return "{}".format(self.message)
