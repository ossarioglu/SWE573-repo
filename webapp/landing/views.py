from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout

from .models import Offering, Tag
from .forms import OfferForm
# My views


def signinPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is not matching')

    context = {}
    return render(request, 'landing/signup_in.html', context)

def signOut(request):
    logout(request)
    return redirect('home')

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
    return render(request, 'landing/home.html', context)

def offerings(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
#    offer : None
#    for i in offers:
#        if i['id'] == int(ofnum):
#            offer = i
    context = {'offers':offer}
    return render(request, 'landing/offerings.html', context)
#    return HttpResponse('Offering Page')

@login_required(login_url='login')
def createOffer(request):
    form = OfferForm()
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.providerID = request.user
            offer.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'landing/create_offering.html', context)

@login_required(login_url='login')
def updateOffer(request, ofNum):

    offer = Offering.objects.get(serviceID=ofNum)
    form = OfferForm(instance=offer)

    if request.user != offer.providerID:
        return HttpResponse('You are not allowed to update this offer')

    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'landing/create_offering.html', context)

@login_required(login_url='login')
def deleteOffer(request, ofNum):
    offer = Offering.objects.get(serviceID=ofNum)
    
    if request.user != offer.providerID:
        return HttpResponse('You are not allowed to delete this offer')

    if request.method == 'POST':
        offer.delete()
        return redirect('home')
    return render(request, 'landing/delete.html', {'obj':offer})