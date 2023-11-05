from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


from .models import User, Room, Message

import requests
from datetime import datetime, timedelta

def registerUser(request):
    status = 'registration'
    endpoint = ('http://127.0.0.1:8000/api/users/create/')

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password1': request.POST['password1'],
            'password2': request.POST['password2'],
        }

        responce = requests.post(endpoint, json=data)
        return redirect(reverse('pre-verification') + f"?un={data.get('username')}&e={data.get('email')}&status={responce.status_code}")
        
    context = {'title':'Registration', 'status': status}
    return render(request, 'main/login_register/login_register.html', context)

def preVerification(request):
    status = request.GET.get('status')
    username = request.GET.get('un')
    email = request.GET.get('e')

    try:
        user = User.objects.get(email=email)
    except:
        user = None
        
    if status == '201' and user != None:
        status = 'verification'

        context = {'status':status, 'username':username, 'email':email,} 
        return render(request, 'main/login_register/login_register.html', context)
    elif status != '201' and user == None and username and email:
        return HttpResponseBadRequest('Something went wrong. Try registration again')
    else:
        return HttpResponseBadRequest('Page not found')
    
def verification(request, signing):
    signer = TimestampSigner()
    try:
        max_age_seconds = 60
        data = signer.unsign_object(signing, max_age=max_age_seconds)

        user = User.objects.get(email=data['email'])
        user.is_active = True
        user.save()

        status = 'success'
    except SignatureExpired:
        status = 'expired'
    except BadSignature:
        status = None
    
    context = {'status':status}
    return render(request, 'main/login_register/email_verification.html', context)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if user is not None and user.is_active == False:
                messages.error(request, 'This account is not activated, because email verification is not completed')
            else:
                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Wrong password')
        except:
            messages.error(request, 'User does not exists')

        
    context = {'page': page, 'title':page.title()}
    return render(request, 'main/login_register/login_register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'main/home_page/home.html', context)

@login_required(login_url='login')
def room(request, id):
    try:
        date = datetime.utcnow()

        room = Room.objects.get(id=id)
        chosen = True

        if request.method == "POST":
            body = request.POST.get("body")
            Message.objects.create(
                host=request.user,
                room=room,
                body=body
            )
            room.updated = datetime.utcnow()
            room.save()
            return redirect('room', id)
        
        context = {'room': room, 'chosen':chosen, "date": date}
        return render(request, 'main/home_page/home.html', context)
    except:
        return redirect('home')

