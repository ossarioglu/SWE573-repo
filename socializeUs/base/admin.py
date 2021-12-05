from django.contrib import admin

# Register your models here.

from .models import Offering, Feedback

admin.site.register(Offering) 
admin.site.register(Feedback) 
