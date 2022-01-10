from typing import ValuesView
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
# unique identifiers for objects are created with this 
import uuid

# Some fields uses current time for default value
today = timezone.now

# Profile is the object keeping information of users
# This object is an addition to Django's User object. It has additionla information that User object does't have

class Profile(models.Model):
    
    # There are 3 types of user
    USER_TYPES = [
        ("user", "user"),
        ("admin", "admin"),
        ("mentor", "mentor"),
    ]

    # user has one-to-one relatiınship with User object
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    userType = models.CharField(max_length=10,choices=USER_TYPES,default='user')
    # user rating is kept at this field
    userReputation = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    creditAmount = models.PositiveIntegerField(editable=True,default=5)
    userDetails = models.TextField(max_length=200,null=True)
    userLocation = models.CharField(max_length=50)
    userPicture = models.ImageField(upload_to='Profiles',null=True, default="male.png")
    # credits are blocked at this field for applied services that are not concluded
    creditInprocess = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.user.username}'
    
    # This is the method to update user's credit Amount
    # Credit amount is restristed to be max 15 in order to motivate user's to get services as well (not only providing)
    def updateCredit(self, amount):
        self.creditAmount += amount
        if self.creditAmount > 15:
            self.creditAmount = 15
        return True
    def blockCredit(self, amount):
        self.creditInprocess += amount
    def checkCredit(self, amount):
        return ((self.creditAmount + self.creditInprocess) >= amount)

# This is the category object
class Tag(models.Model):
    tagName = models.CharField(primary_key = True,max_length=15)
    def __str__(self):
        return self.tagName

# This is the service object
# Initially it's decided to have 2 different objects for Offerring and Events
# However, it's noticed that they could be both managed at same object with serviceType field
class Offering(models.Model):

    # This is for Service Status options
    SERVICE_STATUS = [
        ("New", "New"),
        ("Closed", "Closed"),
        ("Assigned", "Assigned"),
    ]

    # This is for Service Type options
    SERVICE_TYPE = [
        ("Offering", "Offering"),
        ("Event", "Event"),
    ]

    # This is for Recurrence Period options
    RECURRENCE_PERIOD = [
        ("None", "None"),
        ("Weekly", "Weekly"),        
        ("Monthly", "Monthly"),
    ]

    # This is for Meeting Type options
    MEETING_TYPE = [
        ("FaceToFace", "FaceToFace"),
        ("Online", "Online"),        
    ]

    # serviceId is created as unique id from UUID object
    serviceID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    #tag (category) has a One-to-Many relation with Tag object: a service can one tag from many tags
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10,choices=SERVICE_STATUS, default='New', editable = True)
    
    # provider has a One-to-Many relation with User object: a service is provider from a user from many Users
    providerID = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(editable=True, max_length=100)
    picture = models.ImageField(upload_to='Services', null=True, default="Cat03.png")
    serviceInfo = models.TextField(max_length=200,null=True,blank=True)
    startingDate = models.DateTimeField(editable=True,default=today)
    duration = models.PositiveIntegerField(editable=True,default=1)
    meetingType = models.CharField(max_length=10,choices=MEETING_TYPE, default='FaceToFace', editable = True)
    location = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(editable=True,default=1)
    recurrance = models.PositiveIntegerField(editable=True,default=1)
    recurrancePeriod = models.CharField(max_length=100,choices=RECURRENCE_PERIOD, default='None')
    deadlineForUpdate = models.DateTimeField(editable=True,default=today)
    # serviceType diverses it as Offering or Event
    serviceType = models.CharField(max_length=100,choices=SERVICE_TYPE, default='Offering')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Services are listed with order with recent activiy having highest order
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return f'{self.serviceID}'

# This object is to keep information on feedbacks while confirming services are done
class Feedback(models.Model):
    
    # There are 5 rating options
    FEEDBACK_RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    
    # feedbackID is created as unique id from UUID object
    feedbackID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    #serviceID has a One-to-Many relation with Service object: a service is one service from many Services
    serviceID = models.ForeignKey(Offering,related_name='feedbackForService', on_delete=models.CASCADE)
    # giverID has a One-to-Many relation with User object: a feedback is given from a user from many Users
    giverID = models.ForeignKey(User, related_name='feedbackGiverID', on_delete=models.CASCADE)
    # takerID has a One-to-Many relation with User object: a feedback is taken from a user from many Users
    takerID = models.ForeignKey(User, related_name='feedbackReceiverID', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(editable=True,choices=FEEDBACK_RATING, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.feedbackID}'

# This object is to keep information for applications to services
class Requestservice(models.Model):
    
    # There are 3 states for requests
    REQUEST_STATUS = [
        ("Inprocess", "Inprocess"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    # requestID is created as unique id from UUID object
    requestID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    # serviceID has a One-to-Many relation with Service object: a service is one service from many Services
    serviceID = models.ForeignKey(Offering, on_delete=models.CASCADE)
    # requesterID has a One-to-Many relation with User object: a service is requested by one user from many Users
    requesterID = models.ForeignKey(User, on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.requestID}'

# This object is to keep information for notifications during processes
class Notification(models.Model):
    
    # There are 2 states for requests
    NOTE_STATUS = [
        ("Unread", "Unread"),
        ("Read", "Read"),
    ]

    # noteID is created as unique id from UUID object
    noteID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    # serviceID has a One-to-Many relation with Service object: a service is one service from many Services
    serviceID = models.ForeignKey(Offering, on_delete=models.CASCADE)
    # receiverID has a One-to-Many relation with User object: a notificiation is received by one user from many Users
    receiverID = models.ForeignKey(User, related_name='receiverID', on_delete=models.CASCADE)
    noteContent = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=NOTE_STATUS,default='Unread')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.noteID}'

# This object is to keep information for notifications during processes
class Assignment(models.Model):
    
    # There are 3 states for requests
    ASSIGNMENT_STATUS = [
        ("Open", "Open"),
        ("Confirmed by provider", "Confirmed by provider"),
        ("Confirmed by receiver", "Confirmed by receiver"),
        ("Closed", "Closed"),
    ]
    
    # assignID is created as unique id from UUID object
    assignID = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    # requestID has a One-to-Many relation with Request object: a request can be assigned from one reques from many Request
    requestID = models.ForeignKey(Requestservice, on_delete=models.CASCADE)
    # approverID has a One-to-Many relation with User object: a assignment is approved by one user from many Users
    approverID = models.ForeignKey(User, related_name='approverForAssignementID',  on_delete=models.CASCADE)
    # requesterID has a One-to-Many relation with User object: a assignment is requested by one user from many Users    
    requesterID = models.ForeignKey(User, related_name='requesterForAssignementID',  on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=ASSIGNMENT_STATUS,default='Open')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.assignID}'
