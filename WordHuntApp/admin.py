# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from WordHuntApp.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Image)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Word)
admin.site.register(Competition)
