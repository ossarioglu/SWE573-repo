from django.contrib import admin

# Register your models here.

from .models import Offering, Feedback, Profile, Tag

admin.site.register(Offering) 
admin.site.register(Feedback) 
admin.site.register(Tag)
admin.site.register(Profile)