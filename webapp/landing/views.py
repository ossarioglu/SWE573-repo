from typing import ContextManager, DefaultDict
from django.forms.widgets import NullBooleanSelect
from django.http.request import split_domain_port
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
import datetime as mydatetime

from django.utils.dateparse import parse_datetime


from .models import Feedback, Offering, Tag, Profile , Requestservice, Notification, Assignment
from .forms import OfferForm, ProfileForm
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
            
            newProfile = Profile.objects.create(user=user, userLocation=request.POST.get('location'))
            newProfile.save()

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
    offer_count = offers.filter(status='New').count()
    if request.user.is_authenticated:
        unreadNote = request.user.receiverID.filter(status='Unread').count
    else:
        unreadNote = ""

    context = {'offers':offers, 'tags':tags, 'offer_count':offer_count,'users':users, 'notes':unreadNote}
    return render(request, 'landing/home.html', context)

@login_required(login_url='login')
def offerings(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
    application = Requestservice.objects.filter(serviceID=ofnum).filter(requesterID=request.user)
    context = {'offers':offer, "applications":application}
    return render(request, 'landing/offerings.html', context)

def userProfile(request, userKey):
    user = User.objects.get(username=userKey)
    offers = user.offering_set.all()
    context = {'user':user, 'offers':offers}
    return render(request, 'landing/profile.html', context) 

@login_required(login_url='login')
def updateProfile(request, userKey):
    user = User.objects.get(username=userKey)
    myProfile = Profile.objects.get(user=user)

    form = UserCreationForm(instance=user)

    if request.user != user:
        return HttpResponse('You are not allowed to update this profile')

    if request.method == 'POST':

        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.email = request.POST.get('email')
        user.save()

        myProfile.userLocation = request.POST.get('location')
        myProfile.userDetails = request.POST.get('userDetails')
        if request.FILES.get('picture') is not None:
            myProfile.userPicture = request.FILES.get('picture')
        myProfile.save()

        return redirect('home')
        
    context = {'form':form,'myProfile':myProfile, 'user':user}
    return render(request, 'landing/update_profile.html', context)

@login_required(login_url='login')
def createOffer(request, page):
    form = OfferForm()
    myKeywords = Tag.objects.all()
    service = page

    if request.method == 'POST':
        selectCategory = request.POST.get('selectCategory')
        getTag, created = Tag.objects.get_or_create(tagName=selectCategory)

        keywords = request.POST.get('keywords')
        serviceInfo = request.POST.get('serviceInfo')
        duration = request.POST.get('duration')
        capacity = request.POST.get('capacity')
        meetingType = request.POST.get('meetingType')
        location = request.POST.get('location')
        recurrance = request.POST.get('recurrance')
        recurrancePeriod = request.POST.get('recurrancePeriod')
        picture = request.POST.get('picture')
        startingDate = str(request.POST.get('startingDate'))
        deadlineForCancel = str(request.POST.get('deadlineForCancel'))
        startingDate = datetime.strptime(startingDate, '%Y-%m-%d %H:%M')
        deadlineForCancel = datetime.strptime(deadlineForCancel, '%Y-%m-%d %H:%M')

        for i in range(int(recurrance)):

            myService = Offering.objects.create(
                tag=getTag,
                providerID = request.user,
                keywords = keywords,
                picture = picture,
                serviceInfo = serviceInfo,
                startingDate = startingDate,
                duration = duration,
                meetingType = meetingType,
                location = location,
                capacity = capacity,
                recurrance = 1,
                recurrancePeriod = 'None',
                deadlineForUpdate = deadlineForCancel,
                serviceType = service
            )
            if myService:
                myService.save()
            
            if recurrancePeriod == 'Weekly':
                startingDate = startingDate + mydatetime.timedelta(days=7)
                deadlineForCancel = deadlineForCancel + mydatetime.timedelta(days=7)
            elif recurrancePeriod == 'Monthly':
                startingDate = startingDate + mydatetime.timedelta(days=30)
                deadlineForCancel = deadlineForCancel + mydatetime.timedelta(days=30)

        return redirect('home')

    context = {'form': form, 'myTags':myKeywords, 'page':service}
    return render(request, 'landing/create_offering.html', context)

@login_required(login_url='login')
def updateOffer(request, ofNum):

    myKeywords = Tag.objects.all()
    offer = Offering.objects.get(serviceID=ofNum)
    form = OfferForm(instance=offer)    

    if request.user != offer.providerID:
        return HttpResponse('You are not allowed to update this offer')

    if request.method == 'POST':

        selectCategory = request.POST.get('selectCategory')
        getTag, created = Tag.objects.get_or_create(tagName=selectCategory)
        offer.tag = getTag
        offer.keywords = request.POST.get('keywords')
        offer.serviceInfo = request.POST.get('serviceInfo')
        offer.startingDate = request.POST.get('startingDate')
        offer.duration = request.POST.get('duration')
        offer.capacity = request.POST.get('capacity')
        offer.meetingType = request.POST.get('meetingType')
        offer.location = request.POST.get('location')
        offer.recurrance = request.POST.get('recurrance')
        offer.recurrancePeriod = request.POST.get('recurrancePeriod')
        offer.deadlineForUpdate = request.POST.get('deadlineForCancel')
        if request.FILES.get('picture') is not None:
            offer.picture = request.FILES.get('picture')
        offer.save()
        return redirect('home')
        
    context = {'form':form,'myTags':myKeywords,'offer':offer}
    return render(request, 'landing/edit_offering.html', context)

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
def requestOffer(request, sID):
    offer = Offering.objects.get(serviceID=sID)

    if (request.user.profile.creditAmount + request.user.profile.creditInprocess) >= offer.duration :

        if not Requestservice.objects.filter(serviceID=offer).filter(requesterID=request.user).exists():
            newrequest = Requestservice.objects.create(serviceID=offer, requesterID=request.user, serviceType=offer.serviceType, status='Inprocess')
            if newrequest:
                blkQnt = offer.duration
                request.user.profile.blockCredit(-blkQnt)
                request.user.profile.save()

                #offer.providerID.profile.blockCredit(blkQnt)
                #offer.providerID.profile.save()

                newnote = Notification.objects.create(
                    serviceID=offer, 
                    receiverID=offer.providerID, 
                    noteContent=request.user.username+' applied for ' 
                                + offer.keywords,
                                status='Unread'
                    )
                            
                if newnote:
                    application = Requestservice.objects.filter(serviceID=sID).filter(requesterID=request.user)
                    context = {'offers':Offering.objects.get(serviceID=sID), "applications":application}
                    return render(request, 'landing/offerings.html', context)
            else:
                return HttpResponse("A problem occured. Please try again later")
        else:
            application = Requestservice.objects.filter(serviceID=sID).filter(requesterID=request.user)
            context = {'offers':Offering.objects.get(serviceID=sID), "applications":application}
            return render(request, 'landing/offerings.html', context)
    else:
        textMessage = "Not Enough Credit"
        application = Requestservice.objects.filter(serviceID=sID).filter(requesterID=request.user)
        context = {'offers':Offering.objects.get(serviceID=sID), "applications":application, "textMessage":textMessage}
        return render(request, 'landing/offerings.html', context)

@login_required(login_url='login')
def deleteRequest(request, rID):
    reqSrvs = Requestservice.objects.get(requestID=rID)
    offer = reqSrvs.serviceID
    providerUser = offer.providerID
    blkQnt= offer.duration

    requestingUser = request.user

    context = {'obj':reqSrvs, 'providerUser':providerUser,'requestingUser':requestingUser, 'blockedQnt':blkQnt}

    if request.user != reqSrvs.requesterID:
        return HttpResponse('You are not allowed to delete this offer')

    if request.method == 'POST':
        reqSrvs.delete()

        blkQnt = offer.duration
        request.user.profile.blockCredit(+blkQnt)
        request.user.profile.save()

        return redirect('home')
    return render(request, 'landing/cancelRequest.html', context)

@login_required(login_url='login')
def assigning(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
    application = Requestservice.objects.filter(serviceID=ofnum)
    allAccepted = Requestservice.objects.filter(status='Accepted').filter(serviceID=offer).count()
    remainingCapacity = offer.capacity - allAccepted

    context = {'offers':offer, 'applications':application, "remainingCapacity":remainingCapacity}
    return render(request, 'landing/assignment.html', context)
#    return HttpResponse('Offering Page')

@login_required(login_url='login')
def assignService(request,sID, rID, uID, sType):
    myRequest = Requestservice.objects.get(requestID=rID)

    if myRequest.status == 'Inprocess':
        newassignment = Assignment.objects.create(
                requestID=myRequest, 
                approverID=request.user, 
                requesterID=myRequest.requesterID, 
                serviceType=myRequest.serviceID.serviceType, 
                status="Open"
            )    

        if newassignment:
            # inprogress credit
            newassignment.requestID.serviceID.status = 'Assigned'
            newassignment.save()
            
            myRequest.status = 'Accepted'
            myRequest.save()

            allAccepted = Requestservice.objects.filter(status='Accepted').filter(serviceID=myRequest.serviceID).count()
            remainingCapacity = newassignment.requestID.serviceID.capacity - allAccepted

            newnote = Notification.objects.create(
                    serviceID=myRequest.serviceID, 
                    receiverID=myRequest.requesterID, 
                    noteContent=request.user.username
                                +' approved your request for '
                                + myRequest.serviceID.keywords, 
                    status='Unread'
                )
            if newnote:

                if remainingCapacity == 0:
                    openRequests = Requestservice.objects.filter(status='Inprocess').filter(serviceID=myRequest.serviceID)
                    
                    for openRqst in openRequests:
                        openRqst.status = 'Rejected'
                        openRqst.save()

                        blkQnt = openRqst.serviceID.duration
                        openRqst.requesterID.profile.blockCredit(+blkQnt)
                        openRqst.requesterID.profile.save()
                        
                        newnote = Notification.objects.create(
                                serviceID=openRqst.serviceID, 
                                receiverID=openRqst.requesterID, 
                                noteContent=request.user.username
                                            +' could not acceept your request for '
                                            + myRequest.serviceID.keywords
                                            +' due to capacity constraints',
                                status='Unread'
                            )

                application = Requestservice.objects.filter(serviceID=myRequest.serviceID)
                context = {'offers':myRequest.serviceID, "applications":application, "remainingCapacity":remainingCapacity}
                return render(request, 'landing/assignment.html', context)
        else:
            return HttpResponse("A problem occured. Please try again later")
    else:
        return redirect('home')
@login_required(login_url='login')
def handshaking(request):
    providedAssignment = Assignment.objects.filter(approverID=request.user)
    receivedAssignment = Assignment.objects.filter(requesterID=request.user)

    context = {'providedAssignments':providedAssignment, "receivedAssignments":receivedAssignment}
    return render(request, 'landing/handshake.html', context)
#    return HttpResponse('Offering Page')

@login_required(login_url='login')
def confirmation(request, asNum):
    myAssignment = Assignment.objects.get(assignID=asNum)

    if request.method == 'POST':
        pID = request.user
        if myAssignment.requestID.serviceID.providerID == request.user:
            rID = myAssignment.requestID.requesterID
            if myAssignment.status == 'Open':
                aStatus = "Confirmed by provider"
            elif myAssignment.status == 'Confirmed by receiver':
                aStatus = "Closed"
        else:
            rID = myAssignment.requestID.serviceID.providerID
            if myAssignment.status == 'Open':
                aStatus = "Confirmed by receiver"
            elif myAssignment.status == 'Confirmed by provider':
                aStatus = "Closed"
        
        feedback = Feedback.objects.create(
            serviceID=myAssignment.requestID.serviceID, 
            giverID=pID, 
            takerID=rID, 
            comment= request.POST.get('offerComment'),
            rating=request.POST.get('sRate')
            )
        if feedback:
            myAssignment.status=aStatus
            myAssignment.save()
            if aStatus == "Closed":
                myAssignment.requestID.serviceID.status = 'Closed'
                myAssignment.requestID.serviceID.save()

                blkQnt = myAssignment.requestID.serviceID.duration
                myAssignment.requestID.serviceID.providerID.profile.updateCredit(+blkQnt)
                myAssignment.requestID.serviceID.providerID.profile.save()

                allRequests = Requestservice.objects.filter(serviceID=myAssignment.requestID.serviceID)

                for myRequest in allRequests:
                    if myRequest.status == "Accepted":
                        myRequest.requesterID.profile.updateCredit(-blkQnt)
                        myRequest.requesterID.profile.blockCredit(+blkQnt)
                        myRequest.requesterID.profile.save()    

            Notification.objects.create(
                serviceID=myAssignment.requestID.serviceID, 
                receiverID=rID, 
                noteContent=request.user.username+ ' confirmed that service has happened for ' + myAssignment.requestID.serviceID.keywords , status='Unread')
  
        return redirect('confirmService', asNum = myAssignment.assignID )

    myFeedback = Feedback.objects.filter(serviceID=myAssignment.requestID.serviceID).order_by('-created')

    context = {'myAssignment':myAssignment, 'myFeedbacks':myFeedback }
    return render(request, 'landing/confirm.html', context)

@login_required(login_url='login')
def notifications(request):
    myNotes = request.user.receiverID.filter()
    context = {'myNotes':myNotes }
    return render(request, 'landing/notification.html', context)

@login_required(login_url='login')
def changeNote(request, nID):
    myNotes = request.user.receiverID.filter()
    myNote = Notification.objects.get(noteID=nID)
    
    if myNote.status == "Read":
        myNote.status = "Unread"
    else:
        myNote.status = "Read"
    myNote.save()

    context = {'myNotes':myNotes }
    return render(request, 'landing/notification.html', context)