from django.urls import path
from . import views

# These are URL patterns that webpage URL is to visit, parameters of these URL and action (views) done when visiting this URL 
urlpatterns = [

    # URL for home page
    path('', views.home, name="home"),

    # URLs for user interactions : login, logout, sign-up, listing profile info, or updating profile
    path('login/', views.signinPage, name="login"),
    path('logout/', views.signOut, name="logout"),
    path('signup/', views.signUpPage, name="signup"),
    path('profile/<str:userKey>/', views.userProfile, name ="user-profile"), 
    path('update-profile/<str:userKey>/', views.updateProfile, name ="update-profile"), 

    # URLs for service activities : listing, create, update and delete
    path('offerings/<str:ofnum>/', views.offerings, name ="offerings"), 
    path('create-offer/<str:page>/', views.createOffer, name ="create-offer"), 
    path('update-offer/<str:ofNum>/', views.updateOffer, name ="update-offer"), 
    path('delete-offer/<str:ofNum>/', views.deleteOffer, name ="delete-offer"), 

    # URLs for application to services : requesting and deleting request
    path('requests/<str:sID>/', views.requestOffer, name ="request-Service"), 
    path('requests/delete/<str:rID>/', views.deleteRequest, name ="delete-Request"), 
    
    # URLs for assigning to services : listing and assigning request
    path('assignment/<str:ofnum>/', views.assigning, name ="assign"), 
    path('assignment/<str:sID>/<str:rID>/<str:uID>/<str:sType>/', views.assignService, name ="assign-Service"), 

    # URLs for handshaking process: listing and confirming assignments
    path('handshake/', views.handshaking, name ="handshake"), 
    path('confirm/<str:asNum>/', views.confirmation, name ="confirmService"), 
   
    # URLs for notification process: listing and updating
    path('notification/', views.notifications, name ="notifications"), 
    path('notification/<str:nID>/', views.changeNote, name ="changeNote"), 

]


