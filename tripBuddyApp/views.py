from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, UserManager, Trip, TripManager
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    registerErrors = User.objects.register_validation(request.POST)
    if len(registerErrors) > 0:
        for error, message in registerErrors.items():
            messages.error(request, message)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['user_pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first=request.POST['first_name'], last=request.POST['last_name'], email=request.POST['user_email'], password=hashed)
        request.session['user_logged'] = newUser.first
        request.session['user_id'] = newUser.id
        request.session['new_user'] = True
        return redirect('/travels')

def login(request):
    loginErrors = User.objects.login_validation(request.POST)
    if len(loginErrors) > 0:
        for error, message in loginErrors.items():
            messages.error(request, message)
        return redirect('/')
    else:
        validUser = User.objects.get(email=request.POST['login_email'])
        request.session['user_logged'] = validUser.first
        request.session['user_id'] = validUser.id
        request.session['est_user'] = True
        return redirect('/travels')

def success(request):
    if request.session['new_user'] == False and request.session['est_user'] == False:
        return redirect('/')
    else:
        context = {
            'userTrip': User.objects.get(id=request.session['user_id']).participate.all(),
            'otherTrip': Trip.objects.exclude(participants=User.objects.get(id=request.session['user_id'])),
        }
        return render(request, 'travels.html', context)

def logout(request):
    request.session['user_logged'] = ''
    del request.session['user_id']
    request.session['new_user'] = False
    request.session['est_user'] = False
    return redirect('/')

def tripForm(request):
    return render(request, 'addTrip.html')

def createTrip(request):
    newTripErrors = Trip.objects.new_trip_validation(request.POST)
    if len(newTripErrors) > 0:
        for error, message in newTripErrors.items():
            messages.error(request, message)
        return redirect('/addtrip')
    else:
        newTrip = Trip.objects.create(destination=request.POST['trip_dest'], description=request.POST['trip_desc'], tripStart=request.POST['trip_start'], tripEnd=request.POST['trip_end'], organized_by=User.objects.get(id=request.session['user_id']))
        newTrip.participants.add(User.objects.get(id=request.session['user_id']))
        return redirect(f'/view/{newTrip.id}')

def viewTrip(request, tripID):
    context = {
        'viewTrip': Trip.objects.get(id=tripID),
        'otherUsers': Trip.objects.get(id=tripID).participants.exclude(id=Trip.objects.get(id=tripID).organized_by.id)
    }
    return render(request, 'viewTrip.html', context)

def joinTrip(request, tripID):
    User.objects.get(id=request.session['user_id']).participate.add(Trip.objects.get(id=tripID))
    return redirect('/travels')

def cancelTrip(request, tripID):
    User.objects.get(id=request.session['user_id']).participate.remove(Trip.objects.get(id=tripID))
    return redirect('/travels')

def deleteTrip(request, tripID):
    delTrip = Trip.objects.get(id=tripID)
    delTrip.delete()
    return redirect('/travels')