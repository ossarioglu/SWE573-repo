from django.shortcuts import render
from django.http import HttpResponse

from .models import Offering
# My views

offers = [
    {'id':1, 'name':'Lets Cook'},
    {'id':2, 'name':'Math is the secret of life'},
    {'id':3, 'name':'Look upto Sky'},
]

def home(request):
    offers = Offering.objects.all()
    context = {'offers':offers}
    return render(request, 'base/home.html', context)

def offerings(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
#    offer : None
#    for i in offers:
#        if i['id'] == int(ofnum):
#            offer = i
    context = {'offers':offer}
    return render(request, 'base/offerings.html', context)
#    return HttpResponse('Offering Page')

