from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('offerings/<str:ofnum>/', views.offerings, name ="offerings"), 
    path('create-offer/', views.createOffer, name ="create-offer"), 

]