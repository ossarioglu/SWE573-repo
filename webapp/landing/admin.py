from django.contrib import admin

# Register your models here.

from .models import Assignment, Offering, Feedback, Profile, Tag , Requestservice, Notification

admin.site.register(Offering) 
admin.site.register(Feedback) 
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Requestservice)
admin.site.register(Notification)
admin.site.register(Assignment)
