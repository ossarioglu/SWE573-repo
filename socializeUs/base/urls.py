from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.signinPage, name="login"),
    path('logout/', views.signOut, name="logout"),

    path('', views.home, name="home"),
    path('offerings/<str:ofnum>/', views.offerings, name ="offerings"), 
    path('create-offer/', views.createOffer, name ="create-offer"), 
    path('update-offer/<str:ofNum>/', views.updateOffer, name ="update-offer"), 
    path('delete-offer/<str:ofNum>/', views.deleteOffer, name ="delete-offer"), 
    path('delete-offer/<str:ofNum>/', views.deleteOffer, name ="delete-offer"), 

]