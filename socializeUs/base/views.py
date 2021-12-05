from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Offering
from .forms import OfferForm
# My views


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

def createOffer(request):
    form = OfferForm()
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/create_offering.html', context)
