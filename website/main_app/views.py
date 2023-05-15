from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .decorators import unauthenticated
from django.contrib import messages
from .models import *
import requests
import json

# Registrations functionality
@unauthenticated
def registration(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        d_number = request.POST.get('device_number')
        contacts = request.POST.get('contacts')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm')


        if pass1 == pass2:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'Username alread exist')
                return redirect('register')
            if Device.objects.filter(device_number=d_number).exists():
                messages.info(request, 'Device number alread exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=name, password=pass1)
                device = Device.objects.create(device_user=user, device_number=d_number, contacts=contacts)
                user.save()
                device.save()
                messages.success(request, 'Device successful registerd for ' + name)
                return redirect('login')
        else:
            messages.error(request, 'Error: Password missmatch')
            return redirect('register')
    else:
        return render(request, 'register.html')

# Login functionality
@unauthenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

# Logout method
def logout_user(request):
    logout(request)
    return redirect('login')

# Home page functionality
@login_required(login_url='login')
def home_page(request):
    # Declatation of variable arrays to store datas
    user_ids = []
    username = []
    device_number = []
    heart_rate = []
    body_temperature = []
    request_data = []
    contacts = []
    
    devices = Device.objects.filter(device_user = request.user.pk)
    device_request = Request.objects.filter(device__in = devices)

    for req in device_request:
        user_ids.append(req.device.device_user.pk)
        username.append(req.device.device_user.username)
        device_number.append(req.device.device_number)
        heart_rate.append(req.heat_rate)
        body_temperature.append(req.body_temp)
        contacts.append(req.device.contacts)

    for id, user, dev, rate, temp, conts in zip(
        user_ids, username, device_number, heart_rate, body_temperature, contacts):
        data = {
            'id': id,
            'username': user,
            'device_number': dev,
            'heart_rate': rate,
            'body_temperature': temp,
            'contacts': conts,
        }
        request_data.append(data)


    return render(request, 'home.html', {'informations': request_data})

@login_required(login_url='login')
def location_manager(request, id):

    ip = requests.get('https://api.ipify.org?format=json')
    ip_address = json.loads(ip.text)
    location = requests.get('http://ip-api.com/json/' + ip_address['ip'])
    our_location = json.loads(location.text)
   
    context = {
        'location': our_location,
        'user': User.objects.get(pk=id)
    }
    return render(request, 'map.html', {'context': context})