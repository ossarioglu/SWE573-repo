from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import Offering, Tag
from .forms import OfferForm
# My views


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    offers = Offering.objects.filter(
        Q(tag__tagName__icontains=q) |
        Q(keywords__icontains=q) |
        Q(serviceInfo__icontains=q) 
    )

    tags = Tag.objects.all()
    offer_count = offers.count()


    context = {'offers':offers, 'tags':tags, 'offer_count':offer_count}
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

def updateOffer(request, ofNum):
    offer = Offering.objects.get(serviceID=ofNum)
    form = OfferForm(instance=offer)

    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/create_offering.html', context)

def deleteOffer(request, ofNum):
    offer = Offering.objects.get(serviceID=ofNum)
    if request.method == 'POST':
        offer.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':offer})