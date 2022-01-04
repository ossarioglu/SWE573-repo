from typing import ValuesView
from django.db import models
from django.db.models.deletion import CASCADE
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

today = timezone.now

class Profile(models.Model):
    
    USER_TYPES = [
        ("user", "user"),
        ("admin", "admin"),
        ("mentor", "mentor"),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    userType = models.CharField(max_length=10,choices=USER_TYPES,default='user')
    userReputation = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    creditAmount = models.PositiveIntegerField(editable=True,default=10)
    userDetails = models.TextField(max_length=200,null=True)
    userLocation = models.CharField(max_length=50)
    userPicture = models.ImageField(upload_to='Profiles',null=True, default="male.png")
    creditInprocess = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username}'
    def updateCredit(self, amount):
        self.creditAmount += amount
        self.creditInprocess -= amount
        return True
    def blockCredit(self, amount):
        self.creditInprocess += amount
    def checkCredit(self, amount):
        return ((self.creditAmount + self.creditInprocess) >= amount)

# Create your models here.
class Tag(models.Model):
    tagName = models.CharField(primary_key = True,max_length=15)
    def __str__(self):
        return self.tagName

class Offering(models.Model):

    SERVICE_STATUS = [
        ("New", "New"),
        ("Closed", "Closed"),
        ("Assigned", "Assigned"),
    ]

    SERVICE_TYPE = [
        ("Offering", "Offering"),
        ("Event", "Event"),
    ]

    RECURRENCE_PERIOD = [
        ("None", "None"),
        ("Weekly", "Weekly"),        
        ("Monthly", "Monthly"),
    ]

    serviceID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10,choices=SERVICE_STATUS, default='New', editable = False)
    providerID = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(editable=True, max_length=100)
    picture = models.ImageField(upload_to='Services', null=True, default="Cat03.png")
    serviceInfo = models.TextField(max_length=200,null=True,blank=True)
    startingDate = models.DateTimeField(editable=True,default=today)
    duration = models.PositiveIntegerField(editable=True,default=1)
    meetingType = models.CharField(max_length=10,default='FaceToFace')
    location = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(editable=True,default=1)
    recurrance = models.PositiveIntegerField(editable=True,default=1)
    recurrancePeriod = models.CharField(max_length=100,choices=RECURRENCE_PERIOD, default='None')
    deadlineForUpdate = models.DateTimeField(editable=True,default=today)
    serviceType = models.CharField(max_length=100,choices=SERVICE_TYPE, default='Offering')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return f'{self.serviceID}'

class Feedback(models.Model):
    FEEDBACK_RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    feedbackID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    serviceID = models.ForeignKey(Offering,related_name='feedbackForService', on_delete=models.CASCADE)
    giverID = models.ForeignKey(User, related_name='feedbackGiverID', on_delete=models.CASCADE)
    takerID = models.ForeignKey(User, related_name='feedbackReceiverID', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(editable=True,choices=FEEDBACK_RATING, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.feedbackID}'

class Requestservice(models.Model):
    REQUEST_STATUS = [
        ("Inprocess", "Inprocess"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    requestID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    serviceID = models.ForeignKey(Offering, on_delete=models.CASCADE)
    requesterID = models.ForeignKey(User, on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.requestID}'

class Notification(models.Model):
    NOTE_STATUS = [
        ("Unread", "Unread"),
        ("Read", "Read"),
    ]

    noteID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    serviceID = models.ForeignKey(Offering, on_delete=models.CASCADE)
    receiverID = models.ForeignKey(User, related_name='receiverID', on_delete=models.CASCADE)
    noteContent = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=NOTE_STATUS,default='Unread')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.noteID}'

class Assignment(models.Model):
    ASSIGNMENT_STATUS = [
        ("Open", "Open"),
        ("Confirmed by provider", "Confirmed by provider"),
        ("Confirmed by receiver", "Confirmed by receiver"),
        ("Closed", "Closed"),
    ]

    assignID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    requestID = models.ForeignKey(Requestservice, on_delete=models.CASCADE)
    approverID = models.ForeignKey(User, related_name='approverForAssignementID',  on_delete=models.CASCADE)
    requesterID = models.ForeignKey(User, related_name='requesterForAssignementID',  on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=ASSIGNMENT_STATUS,default='Open')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.assignID}'
