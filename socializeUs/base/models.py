from typing import ValuesView
from django.db import models
from django.db.models.deletion import CASCADE
import uuid
from django.utils import timezone

from django.contrib.auth.models import User



# Create your models here.

class Offering(models.Model):
    serviceID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    status = models.CharField(max_length=10,default='New')
    providerID = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=100)
    serviceInfo = models.TextField(max_length=200,null=True,blank=True)
    startingDate = models.DateTimeField(editable=True,default=timezone.now())
    duration = models.PositiveIntegerField(editable=True,default=1)
    meetingType = models.CharField(max_length=10,default='FaceToFace')
    location = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(editable=True,default=1)
    deadlineForUpdate = models.DateTimeField(editable=True,default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.keywords


class Feedback(models.Model):
    feedbackID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    serviceID = models.ForeignKey(Offering, on_delete=models.CASCADE)
    giverID = models.ForeignKey(User, related_name='feedback_give_id', on_delete=models.CASCADE)
    takerID = models.ForeignKey(User, related_name='feedback_receiver_id', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(editable=True,default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:20]
