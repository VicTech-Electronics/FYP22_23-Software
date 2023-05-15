from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import authenticated_user
from django.contrib import messages
from .models import *


@login_required(login_url='login')
def home(request):
    cases = Case.objects.count()
    payed_cases = Case.objects.filter(payment=True).count()
    unpayed_cases = Case.objects.filter(payment=False).count()
    percentage_payed = (payed_cases/cases) * 100
    percentage_unpayed = (unpayed_cases/cases) * 100

    context1 = {
        'cases': cases,
        'payed_cases': payed_cases,
        'unpayed_cases': unpayed_cases,
        'percentage_payed': round(percentage_payed, 2),
        'percentage_unpayed': round(percentage_unpayed, 2),
    }
    
    context2 = Case.objects.all()
    return render(request, 'index.html', {'data':context1, 'infomations':context2})

# Method for user to login
@authenticated_user
def user_login(request):
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

# Methode for the user to logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Registration method for a new details
def registration(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        vehicle_number = request.POST.get('vehicle_no')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        if Driver.objects.filter(vehicle_number=vehicle_number).exists():
            messages.warning(request, 'Vehicle number alread exist')
            return redirect('registration')
        
        driver = Driver.objects.create(username=user, vehicle_number=vehicle_number, email=email, contact=contact)
        driver.save()
        messages.success(request, 'Information added for car number ' + vehicle_number + ', Owned by ' + user)
        return redirect('registration')
    else:
        return render(request, 'register.html')

def manage_location(request, case_id):
    context =  Case.objects.get(pk=case_id)
    return render(request, 'map.html', {'data': context})
