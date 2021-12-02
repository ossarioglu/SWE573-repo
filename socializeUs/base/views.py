from django.shortcuts import render
from django.http import HttpResponse

# My views

def home(request):
    return render(request, 'home.html')

def offerings(request):
    return render(request, 'offerings.html')
#    return HttpResponse('Offering Page')

