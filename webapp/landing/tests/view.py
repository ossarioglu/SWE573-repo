from django.http import response
from django.test import TestCase, Client, client
from landing.views import *
from django.urls import reverse
from landing.models import *
import json
from django.contrib.auth import authenticate,login, logout 
from django.contrib.auth.models import User


class TestAppViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        #This is setup for objects to be used at tests
        cls.user = User.objects.create(username="myTestUser", password="MySecretPass")
        cls.myProfile = Profile.objects.create(user=cls.user,creditAmount=10,creditInprocess=-3)
        cls.myTag = Tag.objects.create(tagName="myTag")
        cls.myOffering = Offering.objects.create(keywords="Python",providerID=cls.user)
        cls.myFeedback = Feedback.objects.create(serviceID=cls.myOffering,giverID=cls.user,takerID=cls.user)
        cls.myRequest = Requestservice.objects.create(serviceID=cls.myOffering,requesterID=cls.user)
        cls.myNote = Notification.objects.create(serviceID=cls.myOffering,receiverID=cls.user)
        cls.myAssignment = Assignment.objects.create(requestID=cls.myRequest,approverID=cls.user,requesterID=cls.user)

        cls.client = Client()
        cls.home_url = reverse('home')
        cls.signInPage_url = reverse('login')
        cls.signup_url = reverse('signup')
        cls.signout_url = reverse('logout')
        cls.handshaking_url = reverse('handshake')
        cls.notification_url = reverse('notifications')
        cls.offering_url = reverse('offerings', kwargs={'ofnum': str(cls.myOffering.serviceID)})
        cls.userProfile_url = reverse('user-profile', kwargs={'userKey': cls.user.username})

    #Testing for checking home url is working
    def test_view_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'landing/home.html')
    
    #Testing for checking sign in url is working
    def test_view_signInPage_GET(self):
        response = self.client.get(self.signInPage_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'landing/signup_in.html')
   
    #Testing for checking sign up url is working
    def test_view_signupPage_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'landing/signup_in.html')

    #Testing for checking logout url is working
    def test_view_logout_GET(self):
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code,302)  

    #Testing for checking userProfile url is working
    def test_view_userProfile_GET(self):
        response = self.client.get(self.userProfile_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'landing/profile.html')
  
    #Testing for login required rule is working when a request is not authenticated
    def test_login_required_GET(self):
        response = self.client.get(self.offering_url)
        self.assertRedirects(response, reverse('login')+'?next='+self.offering_url)

    #Testing for authentication rule is working 
    def test_offering_GET(self):
        username = self.user.username
        password = self.user.password
        print('username:'+username)
        print('password:'+password)
        self.client.login(username=username, password=password)
        print(self.user.is_authenticated)

        response = self.client.get(self.signInPage_url)
        self.assertEqual(response.status_code,200)
