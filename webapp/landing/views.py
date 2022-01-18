
# Necessary libraries for rendering views, user management, and getting and adding data to Forms

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

# Models and Formed used in this app
from .models import Feedback, Offering, Tag, Profile , Requestservice, Notification, Assignment
from .forms import OfferForm,MyRegisterForm


# Sign-in Functionality
def signinPage(request):
    # Same frontend page is used for sign-in and sign-out. Page info is sent for Signin
    page = 'signin'
    
    # If user is already autheticated there is no need for sign-in, so page is redirected to home
    if request.user.is_authenticated:
        return redirect('home')
    
    # When info is entered at the sign-in page, username and password is validated
    # If they match, then user is autenticated, otherwise error message is rendered
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
    
    # Page information is sent to frontend
    context = {'page':page}
    return render(request, 'landing/signup_in.html', context)

# This is basic sign-out feature
def signOut(request):
    logout(request)
    return redirect('home')

# This is for sign-up of new users
def signUpPage(request):
    
    # Customized form for user information is called.
    form = MyRegisterForm()

    # When user details are posted, the information is matched with User model's field
    # Mandatory fields for quick signup is Username, Password, Name and Surname, Email, and Location 
    if request.method == 'POST':
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            login(request,user)
            
    # Django's default user model is used for User management. Therefore for further information about user is stored at Profile model
    # At quick signup, Location is a mandatory field from Profile model
    # New profile for this user is created and saved after adding Location information 
            newProfile = Profile.objects.create(user=user, userLocation=request.POST.get('location'))
            newProfile.save()
    
    # After user is created, page is redirected to home page
    # Error is rendered in case there is problem in sign-up process 
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    
    return render(request, 'landing/signup_in.html', {'form':form})

# This is the home page functionalities
# Whenever a search query is triggered for services, this page retrives results 
# Any visitor can see these information, but actions are restricted at front-end
def home(request):
    
    # This is the keywords for search query 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Built-im Q Object of Django is used for Search queries
    # It search keywords at Category Name (tagName), Name of the service (keywords), and details of service (Service Info)

    offers = Offering.objects.filter(
        Q(tag__tagName__icontains=q) |
        Q(keywords__icontains=q) |
        Q(serviceInfo__icontains=q) 
    )

    # Relevants objects are sent to front-end to build the page: Category names, User Information, New and Closed Service numbers
    tags = Tag.objects.all()
    users = User.objects.all()
    offer_count = offers.filter(status='New').count()
    offer_count_old = offers.filter(status='Closed').count()

    # Number of unread notification is send to main page
    if request.user.is_authenticated:
        unreadNote = request.user.receiverID.filter(status='Unread').count
    else:
        unreadNote = ""

    context = {'offers':offers, 'tags':tags, 'offer_count':offer_count,'users':users, 'notes':unreadNote, 'offer_count_old':offer_count_old}
    return render(request, 'landing/home.html', context)


# This is for creating details of any requested offer.
# Login is required to see details of services 
@login_required(login_url='login')
def offerings(request, ofnum):

    # Queried service is retreived from all services
    offer = Offering.objects.get(serviceID=ofnum)
    
    # This is query for this service id whether authenticated user applied for this service or not
    application = Requestservice.objects.filter(serviceID=ofnum).filter(requesterID=request.user)

    # Serve information, and application info is sent to front-end
    context = {'offers':offer, "applications":application}
    return render(request, 'landing/offerings.html', context)

# This is for seeing user profile details
# Services offered by user is send to front-end
def userProfile(request, userKey):
    user = User.objects.get(username=userKey)
    offers = user.offering_set.all()
    context = {'user':user, 'offers':offers}
    return render(request, 'landing/profile.html', context) 

# This is for updating user profile
# Login is required to see details of services 
@login_required(login_url='login')
def updateProfile(request, userKey):
    
    # Information from User and Profile is retrieved for authenticated user
    user = User.objects.get(username=userKey)
    myProfile = Profile.objects.get(user=user)

    # Authenticated user's information is called to Django's default UserCreation Form
    form = UserCreationForm(instance=user)

    if request.user != user:
        return HttpResponse('You are not allowed to update this profile')

    # When information is posted, it updates the user information for User and Profile models according to form's data
    # Returns back to home page after update is done.
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

# This is creating a Service (Offer or Event). Type of the event is sent with "page" parameter
# Login is required to see details of services 
@login_required(login_url='login')
def createOffer(request, page):

    # OfferForm is called, all possible categories are called, and service type is set as posted 'page' information
    form = OfferForm(request.POST, request.FILES)
    myKeywords = Tag.objects.all()
    service = page

    # If there is post from the form, a new Offering (service) is created all relevant fields are matched with Offering Models fields, and service is saved
    if request.method == 'POST':
        
        # All relevant information from Form are assigned to a variable 

        selectCategory = request.POST.get('selectCategory')
        # If user selects a new category, this is added to categories (Tag)
        getTag, created = Tag.objects.get_or_create(tagName=selectCategory)

        keywords = request.POST.get('keywords')
        serviceInfo = request.POST.get('serviceInfo')
        duration = request.POST.get('duration')
        capacity = request.POST.get('capacity')
        meetingType = request.POST.get('meetingType')
        location = request.POST.get('location')
        recurrance = request.POST.get('recurrance')
        recurrancePeriod = request.POST.get('recurrancePeriod')
        picture = request.FILES.get('picture')
        startingDate = str(request.POST.get('startingDate'))
        deadlineForCancel = str(request.POST.get('deadlineForCancel'))
        startingDate = datetime.strptime(startingDate, '%Y-%m-%d %H:%M')
        deadlineForCancel = datetime.strptime(deadlineForCancel, '%Y-%m-%d %H:%M')

        # Based on the number of recurrance of the service, there is a loop to create new services        
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
                if request.FILES.get('picture') is not None:
                    myService.picture = request.FILES.get('picture')
                    myService.save()

            
            # Based on the selected period, event start date and deadline for changes are updated for next iteration 
            if recurrancePeriod == 'Weekly':
                startingDate = startingDate + mydatetime.timedelta(days=7)
                deadlineForCancel = deadlineForCancel + mydatetime.timedelta(days=7)
            elif recurrancePeriod == 'Monthly':
                startingDate = startingDate + mydatetime.timedelta(days=30)
                deadlineForCancel = deadlineForCancel + mydatetime.timedelta(days=30)

        return redirect('home')

    context = {'form': form, 'myTags':myKeywords, 'page':service}
    return render(request, 'landing/create_offering.html', context)

# This is updating a Service (Offer or Event). Service is called with its unique id
# Login is required to see details of services 
@login_required(login_url='login')
def updateOffer(request, ofNum):

    # Information for requested service is retreived from database, and added to Form
    myKeywords = Tag.objects.all()
    offer = Offering.objects.get(serviceID=ofNum)
    form = OfferForm(instance=offer)    

    if request.user != offer.providerID:
        return HttpResponse('You are not allowed to update this offer')

    # When user posts information from Form, relevant fields are matched with object, and service is saved.
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

# This is deleting a Service (Offer or Event). Service is called with its unique id
# Login is required to see details of services 
@login_required(login_url='login')
def deleteOffer(request, ofNum):
    
    offer = Offering.objects.get(serviceID=ofNum)
    
    if request.user != offer.providerID:
        return HttpResponse('You are not allowed to delete this offer')
    
    #If confirmation from user is posted, record for service is deleted.
    if request.method == 'POST':
        offer.delete()
        return redirect('home')
    return render(request, 'landing/delete.html', {'obj':offer})

# This is for user's applications to service. When user apply for a service, this is triggered. 
# Request for service is done with posting service's unique id
# Login is required to see details of services 
@login_required(login_url='login')
def requestOffer(request, sID):
    offer = Offering.objects.get(serviceID=sID)
    
    # This variable is used for blocking or deducting credits of users
    # As default it's set as 0 for Events, and if service is an Offering then, it's updates as the duration of activity
    creditNeeded = 0
    if offer.serviceType == "Offering":
        creditNeeded = offer.duration

    # User can apply a service only if there is enough credit
    # Since user's credits are blocked at creditInprocess for ongoing services (Open requests, accepted application)
    # available credit is calculated by summing current creditAmount and creditInprocess
    # Events are free activities, so user can apply any Event even if there is no available credit
    if (request.user.profile.creditAmount + request.user.profile.creditInprocess) >= creditNeeded:

        # If user didn't apply the service before, then new request is created
        if not Requestservice.objects.filter(serviceID=offer).filter(requesterID=request.user).exists():
            
            # Status of new requests are Inprocess
            newrequest = Requestservice.objects.create(serviceID=offer, requesterID=request.user, serviceType=offer.serviceType, status='Inprocess')
            if newrequest:
                
                # When a request is created, credits of users are blocked by calling blockCredit method of Profile object

                blkQnt = creditNeeded
                request.user.profile.blockCredit(-blkQnt)
                request.user.profile.save()

                # A notification is created for service provider to inform that user is applied to this service
                newnote = Notification.objects.create(
                    serviceID=offer, 
                    receiverID=offer.providerID, 
                    noteContent=request.user.username+' applied for ' 
                                + offer.keywords,
                                status='Unread'
                    )

                # After notification is created, user is sent back to services information page
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
    
    # If user doesn't have enough credit, this state is sent to front-end as a message variable during render
    else:
        textMessage = "Not Enough Credit"
        application = Requestservice.objects.filter(serviceID=sID).filter(requesterID=request.user)
        context = {'offers':Offering.objects.get(serviceID=sID), "applications":application, "textMessage":textMessage}
        return render(request, 'landing/offerings.html', context)

# This is for cancelling user's applications.
# Cancellation for request is done with request's unique id
# Login is required to see details of services 
@login_required(login_url='login')
def deleteRequest(request, rID):
    
    #Information for the queried reques is retrieved.
    reqSrvs = Requestservice.objects.get(requestID=rID)
    offer = reqSrvs.serviceID
    providerUser = offer.providerID
    
    #Credit calculation is done, Events: 0, Offerings:Duration
    creditNeeded = 0
    if offer.serviceType == "Offering":
        creditNeeded = offer.duration
    blkQnt= creditNeeded

    requestingUser = request.user
    context = {'obj':reqSrvs, 'providerUser':providerUser,'requestingUser':requestingUser, 'blockedQnt':blkQnt}

    if request.user != reqSrvs.requesterID:
        return HttpResponse('You are not allowed to delete this offer')

    #If user posts cancellation for request, request is deleted from database
    # Credits blocked for the event is given back to user by updating inprocessCredits 
    if request.method == 'POST':
        reqSrvs.delete()

        blkQnt = creditNeeded
        request.user.profile.blockCredit(+blkQnt)
        request.user.profile.save()

        return redirect('home')
    return render(request, 'landing/cancelRequest.html', context)

# This is for listing assingments for the services
# Login is required to see details of services 
@login_required(login_url='login')
def assigning(request, ofnum):
    offer = Offering.objects.get(serviceID=ofnum)
    application = Requestservice.objects.filter(serviceID=ofnum)
    allAccepted = Requestservice.objects.filter(status='Accepted').filter(serviceID=offer).count()
    
    # Remaning capacity is sent to frontend to avoid more assignments than capacity
    remainingCapacity = offer.capacity - allAccepted

    context = {'offers':offer, 'applications':application, "remainingCapacity":remainingCapacity}
    return render(request, 'landing/assignment.html', context)

# This is for accepting requests and assinging users for the services
# Login is required to see details of services
@login_required(login_url='login')
def assignService(request,sID, rID, uID, sType):

    # Information application to be assigned is retrieved
    myRequest = Requestservice.objects.get(requestID=rID)

    # Application is processed if it's still in 'Inprocess' state
    # New assignment object is created for this application
    if myRequest.status == 'Inprocess':
        newassignment = Assignment.objects.create(
                requestID=myRequest, 
                approverID=request.user, 
                requesterID=myRequest.requesterID, 
                serviceType=myRequest.serviceID.serviceType, 
                status="Open"
            )    
       
        # When assignment is done status for service is updated as 'Assigned', and application status is updated as 'Accepted'
        if newassignment:

            newassignment.requestID.serviceID.status = 'Assigned'
            newassignment.save()
            
            myRequest.status = 'Accepted'
            myRequest.save()

            # Remaining capacity is calculated by deducting all accepted request.

            allAccepted = Requestservice.objects.filter(status='Accepted').filter(serviceID=myRequest.serviceID).count()
            remainingCapacity = newassignment.requestID.serviceID.capacity - allAccepted

            # New notification is created for requesters to inform that the application is accepted, and request is approved
            newnote = Notification.objects.create(
                    serviceID=myRequest.serviceID, 
                    receiverID=myRequest.requesterID, 
                    noteContent=request.user.username
                                +' approved your request for '
                                + myRequest.serviceID.keywords, 
                    status='Unread'
                )
            if newnote:

                # After the assignment, if there is no availbe capacility, all 'Inprocess' applications' status are updated as 'Rejected'
                # Credits for these applications are released back
                # A notification is sent to requester to inform than application is rejected due to capacity constraint

                if remainingCapacity == 0:
                    openRequests = Requestservice.objects.filter(status='Inprocess').filter(serviceID=myRequest.serviceID)
                    
                    for openRqst in openRequests:
                        openRqst.status = 'Rejected'
                        openRqst.save()

                        # Credits given back
                        creditNeeded = 0
                        if openRqst.serviceID.serviceType == "Offering":
                            creditNeeded = openRqst.serviceID.duration
                        blkQnt= creditNeeded
                        openRqst.requesterID.profile.blockCredit(+blkQnt)
                        openRqst.requesterID.profile.save()
                        
                        # Notification for rejection
                        newnote = Notification.objects.create(
                                serviceID=openRqst.serviceID, 
                                receiverID=openRqst.requesterID, 
                                noteContent=request.user.username
                                            +' could not acceept your request for '
                                            + myRequest.serviceID.keywords
                                            +' due to capacity constraints',
                                status='Unread'
                            )
                
                # User is sent back to assignment page to see updates.
                application = Requestservice.objects.filter(serviceID=myRequest.serviceID)
                context = {'offers':myRequest.serviceID, "applications":application, "remainingCapacity":remainingCapacity}
                return render(request, 'landing/assignment.html', context)
        else:
            return HttpResponse("A problem occured. Please try again later")
    else:
        return redirect('home')



# This is for listing all approved assignment for both provider and receiver
# Login is required to see details of services
@login_required(login_url='login')
def handshaking(request):
    providedAssignment = Assignment.objects.filter(approverID=request.user)
    receivedAssignment = Assignment.objects.filter(requesterID=request.user)

    context = {'providedAssignments':providedAssignment, "receivedAssignments":receivedAssignment}
    return render(request, 'landing/handshake.html', context)


# This is for handshaking, and confirming the service is done, and feedbacks are given to each party. 
# Login is required to see details of services
@login_required(login_url='login')
def confirmation(request, asNum):
    
    # Information is retreived for relevant assignment
    myAssignment = Assignment.objects.get(assignID=asNum)

    # User posts any input for confirmation, these steps are triggered
    if request.method == 'POST':

        # This block is to define whether posting user is receiver or provider for the service
        # Based on the user, state of assignment will be updated
        # State is also affected for previous state of the assignment
        # For instance, if assignment was an 'Open' assignment, meaning there was no process before, it's stated is updated as:
        #  - 'Confirmed by provider' if posting user is provider of service
        #  - 'Confirmed by receiver' if posting user is receiver of service
        # If this assignment was already processed before, it's state becomes 'Closed'

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
        
        # Each user needs to give feedback with a rating to confirm the service is done, and close the assignment
        # Feedback object is created and recorded to database inline to information from the form posting
        feedback = Feedback.objects.create(
            serviceID=myAssignment.requestID.serviceID, 
            giverID=pID, 
            takerID=rID, 
            comment= request.POST.get('offerComment'),
            rating=request.POST.get('sRate')
            )
        if feedback:
            
            # Assignment status is updated
            myAssignment.status=aStatus
            myAssignment.save()

            # If an assignment is closed, this doesn't mean that service is also closed for services having more than 1 participants
            if aStatus == "Closed":

                # All requests for this service is retreived
                allRequests = Requestservice.objects.filter(serviceID=myAssignment.requestID.serviceID)

                # We check whether there is any unclosed assignment for the service
                allAssignedClosedCheck = True
                firstLoopBreak = False
                for myRequest in allRequests:
                    checkedAssignment = Assignment.objects.filter(requestID = myRequest)
                    for chAssgn in checkedAssignment:
                        if chAssgn.status != "Closed":
                            allAssignedClosedCheck = False
                            firstLoopBreak = True
                            break
                    if firstLoopBreak: 
                            break
                
                # If status for all assignments for the service 'Closed', than state of Servie is update as 'Closed'
                if allAssignedClosedCheck:
                    myAssignment.requestID.serviceID.status = 'Closed'
                    myAssignment.requestID.serviceID.save()
                    
                    # Ratings of the users are updated based on their all historic ratings
                    myFeedback = Feedback.objects.filter(takerID=myAssignment.requestID.serviceID.providerID)
                    sumRating = 0.0
                    countRating = 0
                    for feeds in myFeedback:
                        sumRating += feeds.rating
                        countRating += 1
                    myRating = sumRating / countRating

                    # Credits are now deducted given to providers
                    # Provider gets credits only for one service, not from all participants
                    creditNeeded = 0
                    if myAssignment.requestID.serviceID.serviceType == "Offering":
                        creditNeeded = myAssignment.requestID.serviceID.duration
                    blkQnt= creditNeeded
                    myAssignment.requestID.serviceID.providerID.profile.updateCredit(+blkQnt)
                    myAssignment.requestID.serviceID.providerID.profile.userReputation = myRating

                    myAssignment.requestID.serviceID.providerID.profile.save()

                    # Blocked Credits are now deducted from all receivers getting this service  
                    for myRequest in allRequests:
                        if myRequest.status == "Accepted":
                            myFeedback = Feedback.objects.filter(takerID=myRequest.requesterID)
                            sumRating = 0.0
                            countRating = 0
                            for feeds in myFeedback:
                                sumRating += feeds.rating
                                countRating += 1
                            myRating = sumRating / countRating

                            myRequest.requesterID.profile.updateCredit(-blkQnt)
                            myRequest.requesterID.profile.blockCredit(+blkQnt)
                            myRequest.requesterID.profile.userReputation = myRating
                            myRequest.requesterID.profile.save()    

            # Notifications are created for other parties of the assignment 
            Notification.objects.create(
                serviceID=myAssignment.requestID.serviceID, 
                receiverID=rID, 
                noteContent=request.user.username+ ' confirmed that service has happened for ' + myAssignment.requestID.serviceID.keywords , status='Unread')
  
        return redirect('confirmService', asNum = myAssignment.assignID )

    myFeedback = Feedback.objects.filter(serviceID=myAssignment.requestID.serviceID).order_by('-created')

    context = {'myAssignment':myAssignment, 'myFeedbacks':myFeedback }
    return render(request, 'landing/confirm.html', context)

# This is for listing notifications
# Login is required to see details of services
@login_required(login_url='login')
def notifications(request):
    myNotes = request.user.receiverID.filter()
    context = {'myNotes':myNotes }
    return render(request, 'landing/notification.html', context)

# This is for updating status of notifications between 'Read' and 'Unread'
# Login is required to see details of services
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