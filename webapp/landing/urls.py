from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.signinPage, name="login"),
    path('logout/', views.signOut, name="logout"),
    path('signup/', views.signUpPage, name="signup"),

    path('', views.home, name="home"),
    path('offerings/<str:ofnum>/', views.offerings, name ="offerings"), 
    path('create-offer/', views.createOffer, name ="create-offer"), 
    path('update-offer/<str:ofNum>/', views.updateOffer, name ="update-offer"), 
    path('delete-offer/<str:ofNum>/', views.deleteOffer, name ="delete-offer"), 
    
    path('profile/<str:userKey>/', views.userProfile, name ="user-profile"), 

    path('requests/<str:sID>/<str:pID>/<str:sType>/', views.requestOffer, name ="request-Service"), 
    path('requests/delete/<str:rID>/<str:pID>/<str:sID>/', views.deleteRequest, name ="delete-Request"), 

    path('assignment/<str:ofnum>/', views.assigning, name ="assign"), 
    path('assignment/<str:sID>/<str:rID>/<str:uID>/<str:sType>/', views.assignService, name ="assign-Service"), 

]


