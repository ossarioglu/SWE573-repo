from typing import ValuesView
from django.db import models
from django.db.models.fields import DurationField
import uuid

from django.utils import timezone


# Create your models here.

class Offering(models.Model):
    serviceID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    status = models.CharField(max_length=10,default='New')
    providerID = models.IntegerField(editable=True)
    keywords = models.CharField(max_length=100)
    serviceInfo = models.CharField(max_length=200,null=True,blank=True)
    startingDate = models.DateTimeField(editable=True,default=timezone.now())
    duration = models.PositiveIntegerField(editable=True,default=1)
    meetingType = models.CharField(max_length=10,default='FaceToFace')
    location = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(editable=True,default=1)
    deadlineForUpdate = models.DateTimeField(editable=True,default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keywords
