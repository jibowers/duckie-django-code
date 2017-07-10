# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Duckling, Quack

# Register your models here.
admin.site.register(Duckling)
admin.site.register(Quack)
