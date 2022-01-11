from django.test import TestCase
from landing.models import Assignment, Feedback, Notification, Offering, Profile, Requestservice, Tag
from django.contrib.auth.models import User

# Unit tests for models at Landing App
class TestAppModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        #This is setup for objects to be used at tests
        cls.user = User.objects.create(username="myTestUser")
        cls.myProfile = Profile.objects.create(user=cls.user,creditAmount=10,creditInprocess=-3)
        cls.myTag = Tag.objects.create(tagName="myTag")
        cls.myOffering = Offering.objects.create(keywords="Python",providerID=cls.user)
        cls.myFeedback = Feedback.objects.create(serviceID=cls.myOffering,giverID=cls.user,takerID=cls.user)
        cls.myRequest = Requestservice.objects.create(serviceID=cls.myOffering,requesterID=cls.user)
        cls.myNote = Notification.objects.create(serviceID=cls.myOffering,receiverID=cls.user)
        cls.myAssignment = Assignment.objects.create(requestID=cls.myRequest,approverID=cls.user,requesterID=cls.user)

    # These tests are to check whether object name will return expected result as model
    # This is for Profile model
    def test_model_Str1(self):
        self.assertEqual(str(self.myProfile),self.user.username)
    
    #This is for Tag model
    def test_model_Str2(self):
        self.assertEqual(str(self.myTag),"myTag")
       
    #This is for Offering model
    def test_model_Str3(self):
        myID = f'{self.myOffering.serviceID}'
        self.assertEqual(str(self.myOffering),myID)

    #This is for Feedback model    
    def test_model_Str4(self):
        myID = f'{self.myFeedback.feedbackID}'  
        self.assertEqual(str(self.myFeedback),myID)

    #This is for Request model
    def test_model_Str5(self):
        myID = f'{self.myRequest.requestID}'  
        self.assertEqual(str(self.myRequest),myID)

    #This is for Notification model
    def test_model_Str6(self):
        myID = f'{self.myNote.noteID}'  
        self.assertEqual(str(self.myNote),myID)

    #This is for Assignment model
    def test_model_Str7(self):
        myID = f'{self.myAssignment.assignID}'  
        self.assertEqual(str(self.myAssignment),myID)

    #Check whether updateCredit method creates right results
    #It also validates credit doesn't exceed MAX_LIMIT 15
    def test_update_credit(self):
        addedCredit = 3
        expectedCredit = 13
        self.myProfile.updateCredit(addedCredit)
        self.assertEqual(self.myProfile.creditAmount,expectedCredit)
        
        addedCredit = 7
        expectedCredit = 15
        self.myProfile.updateCredit(addedCredit)
        self.assertEqual(self.myProfile.creditAmount,expectedCredit)

    #Check whether blockCredit method works properly
    def test_block_credit(self):
        blockedCredit = -1
        expectedResult = -4
        self.myProfile.blockCredit(blockedCredit)
        self.assertEqual(self.myProfile.creditInprocess,expectedResult) 

    #Check whether checkCredit method works properly
    def test_check_credit(self):
        myResult = self.myProfile.checkCredit(7)
        expectedResult = True
        self.assertEqual(myResult,expectedResult) 
    
