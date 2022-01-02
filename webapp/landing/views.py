from typing import ContextManager
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Offering, Tag, Profile , Requestservice, Notification, Assignment
from .forms import OfferForm
# My views


def signinPage(request):
    page = 'signin'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    context = {'page':page}
    return render(request, 'landing/signup_in.html', context)

def signOut(request):
    logout(request)
    return redirect('home')

def signUpPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
            
    return render(request, 'landing/signup_in.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    offers = Offering.objects.filter(
        Q(tag__tagName__icontains=q) |
        Q(keywords__icontains=q) |
        Q(serviceInfo__icontains=q) 
    )

    tags = Tag.objects.all()
    users = User.objects.all()
    offer_count = offers.count()


    context = {'offers':offers, 'tags':tags, 'offer_count':offer_count,'users':users}
    return render(request, 'landing/home.html', context)

def offerings(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
    application = Requestservice.objects.filter(serviceID=ofnum)
#    offer : None
#    for i in offers:
#        if i['id'] == int(ofnum):
#            offer = i
    context = {'offers':offer, "applications":application}
    return render(request, 'landing/offerings.html', context)
#    return HttpResponse('Offering Page')

def userProfile(request, userKey):
    user = User.objects.get(username=userKey)
    offers = user.offering_set.all()
    context = {'user':user, 'offers':offers}
    return render(request, 'landing/profile.html', context) 
    

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

@login_required(login_url='login')
def requestOffer(request, sID, pID, sType):
    newrequest = Requestservice.objects.create(serviceID=Offering.objects.get(serviceID=sID), requesterID=request.user, serviceType=sType, status='New')
    if newrequest:
        offer = Offering.objects.get(serviceID=sID)
        blkQnt = offer.duration
        request.user.profile.blockCredit(-blkQnt)
        request.user.profile.save()

        providerUser = User.objects.get(username=pID)
        providerUser.profile.blockCredit(blkQnt)
        providerUser.profile.save()

        newnote = Notification.objects.create(serviceID=Offering.objects.get(serviceID=sID), receiverID=User.objects.get(username=pID), noteContent=request.user.username+' applied for '+f'{Offering.objects.get(serviceID=sID)}', status='Unread')
        if newnote:
            application = Requestservice.objects.filter(serviceID=sID)
            context = {'offers':Offering.objects.get(serviceID=sID), "applications":application}
            return render(request, 'landing/offerings.html', context)
    else:
        return HttpResponse("A problem occured. Please try again later")

@login_required(login_url='login')
def deleteRequest(request, rID, pID, sID):
    reqSrvs = Requestservice.objects.get(requestID=rID)
    providerUser = User.objects.get(username=pID)
    offer = Offering.objects.get(serviceID=sID)
    blkQnt= offer.duration

    requestingUser = request.user

    context = {'obj':reqSrvs, 'providerUser':providerUser,'requestingUser':requestingUser, 'blockedQnt':blkQnt}

    if request.user != reqSrvs.requesterID:
        return HttpResponse('You are not allowed to delete this offer')

    if request.method == 'POST':
        reqSrvs.delete()
        return redirect('home')
    return render(request, 'landing/cancelRequest.html', context)

def assigning(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
    application = Requestservice.objects.filter(serviceID=ofnum)

    context = {'offers':offer, 'applications':application}
    return render(request, 'landing/assignment.html', context)
#    return HttpResponse('Offering Page')

@login_required(login_url='login')
def assignService(request,sID, rID, uID, sType):
    newassignment = Assignment.objects.create(requestID=Requestservice.objects.get(requestID=rID), approverID=User.objects.get(username=request.user), requesterID=User.objects.get(username=uID), serviceType=sType, status="Open")    
    if newassignment:
        # inprogress credit
        newnote = Notification.objects.create(serviceID=Offering.objects.get(serviceID=sID), receiverID=User.objects.get(username=uID), noteContent=request.user.username+' approved your request for '+f'{Offering.objects.get(serviceID=sID)}', status='Unread')
        if newnote:
            application = Requestservice.objects.filter(serviceID=sID)
            context = {'offers':Offering.objects.get(serviceID=sID), "applications":application}
            return render(request, 'landing/assignment.html', context)
    else:
        return HttpResponse("A problem occured. Please try again later")