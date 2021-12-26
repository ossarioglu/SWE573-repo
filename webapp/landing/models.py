from typing import ValuesView
from django.db import models
from django.db.models.deletion import CASCADE
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    userType = models.CharField(max_length=10)
    userReputation = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    creditAmount = models.PositiveIntegerField(editable=True,default=10)
    userDetails = models.TextField(max_length=200,null=True,blank=True)
    userLocation = models.CharField(max_length=50)
    userPicture = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    creditInprocess = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username}'

# Create your models here.
class Tag(models.Model):
    tagName = models.CharField(primary_key = True,max_length=15)
    def __str__(self):
        return self.tagName

class Offering(models.Model):
    today = timezone.now
    serviceID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10,default='New')
    providerID = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='offer_images', height_field=None, width_field=None, max_length=100, blank=True)
    serviceInfo = models.TextField(max_length=200,null=True,blank=True)
    startingDate = models.DateTimeField(editable=True,default=today)
    duration = models.PositiveIntegerField(editable=True,default=1)
    meetingType = models.CharField(max_length=10,default='FaceToFace')
    location = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(editable=True,default=1)
    recurrance = models.PositiveIntegerField(editable=True,default=1)
    deadlineForUpdate = models.DateTimeField(editable=True,default=today)
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

