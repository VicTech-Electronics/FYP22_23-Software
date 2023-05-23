from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated
from django.contrib import messages
from .models import *
import requests
import json



@login_required(login_url='login')
def home(request):
    context = Informations.objects.all()
    return render(request, 'home.html', {'informations': context})


@unauthenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Hello ' + username + ', You are successful login to the page')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    else:
        return render(request, 'login.html')



@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def details(request, info_id):
     
    ip = requests.get('https://api.ipify.org?format=json')
    ip_address = json.loads(ip.text)
    location = requests.get('http://ip-api.com/json/' + ip_address['ip'])
    our_location = json.loads(location.text)

    context = Informations.objects.get(pk=info_id)

    return render(request, 'details.html', {'our_location': our_location, 'informations': context})