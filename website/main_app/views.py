from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import *
from .models import *
import requests
import json

def home(request):
    return render(request, 'home.html')

@admin_only
def admin_dashboard(request):
    accidents = Accident.objects.all()
    return render(request, 'dashboard.html', {'information': accidents})

@login_required(login_url='login')
@hospital_only
def hospital_dashboard(request):
    hospital = Hospital.objects.filter(user = request.user)
    accidents = Accident.objects.filter(hospital__in = hospital)
    return render(request, 'dashboard.html', {'information': accidents})

@login_required(login_url='login')
@customer_only
def custormer_dashboard(request):
    vehicles = Vehicle.objects.filter(user = request.user)
    accidents = Accident.objects.filter(vehicle__in = vehicles)
    return render(request, 'dashboard.html', {'information': accidents})

@login_required(login_url='login')
def location(request, pk):
    # Accident information from the database
    db_data = Accident.objects.get(id=pk)
    accident_lat = db_data.latitude
    accident_lng = db_data.longitude

    # Accident location informations
    accident_loc_info = requests.get('https://geocode.xyz/' + str(accident_lat) + ',' + str(accident_lng) + '?geoit=json&auth=973956288414548960821x123850')
    accident_loc = json.loads(accident_loc_info.text)

    # Center location informations
    ip_address = json.loads(requests.get('https://api.ipify.org?format=json').text)
    location_info = json.loads(requests.get('http://ip-api.com/json/' + ip_address['ip']).text)

    return render(request, 'location.html', {'accident':accident_loc, 'information':location_info})


# User management
@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        vehicle_number = request.POST.get('vehicle_number')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        check = request.POST.get('check')

        if password1 == password2:
            if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Sorry, The vehicle is alredy registed in the past')
                return redirect('user_reg')
            
            if check:
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(username=username, password=password1)
                group = Group.objects.get(name='custormer')
                user.groups.add(group)
                user.save()
            
            vehicle = Vehicle.objects.create(user=user, vehicle_number=vehicle_number, phone1=phone1, phone2=phone2)
            vehicle.save()
            messages.success(request, 'Registration success')
            return redirect('login')     
        else:
            messages.error(request, 'Password missmatch')
            return redirect('user_reg')
    else:
        return render(request, 'user_reg.html')

# Hospital management
@unauthenticated_user
def register_hospital(request):
    if request.method == 'POST':
        hospital_name = request.POST.get('hospital_name')
        reg_number = request.POST.get('reg_number')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if Hospital.objects.filter(reg_number=reg_number).exists():
                messages.error(request, 'Hospital registration number already exist')
                return redirect('hospital_reg')
            else:
                user = User.objects.create_user(username=hospital_name + ' Hospital', password=password1)  
                hospital = Hospital.objects.create(user=user, reg_number=reg_number, latitude=latitude, longitude=longitude)
                group = Group.objects.get(name='hospital')
                user.groups.add(group)
                hospital.save()
                user.save()

                messages.success(request, 'Registration success')
                return redirect('login')
        else:
            messages.error(request, 'Password mismatch')
            return redirect('hospital_reg')
    else:
        return render(request, 'hospital_reg.html')

# Account management
@unauthenticated_user
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('hospital')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def signout(request):
    logout(request)
    return redirect('home')