from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import *
from .models import *

# Definition of usefull variable
cost_per_unit = 200

# Create your views here.
@login_required(login_url='login')
def home(request):
    customer = Customer.objects.get(user=request.user.pk)
    return render(request, 'home.html', {'context': customer})


# Account management
@unauthenticated_user
def signin(request):
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
    

def signout(request):
    logout(request)
    return redirect('home')

# User management
@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        meter_number = request.POST.get('meter_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username alread exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                customer = Customer.objects.create(user=user, meter_number=meter_number, amount=0.0)
                user.save()
                customer.save()

                messages.success(request, 'Account registered successfull')
                return redirect('login')
        else:
            messages.error(request, 'Password mismatch')
            return redirect('register')
    else:
        print('Method is not POST')
        return render(request, 'register.html')


@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        meter_number = request.POST.get('meter_number')
        amount = float(request.POST.get('amount'))

        if Customer.objects.filter(meter_number = meter_number).exists():
            customer = Customer.objects.get(meter_number = meter_number)
            if amount <= customer.amount:
                customer.amount -= amount
                units_payed = amount / cost_per_unit
                customer.units += units_payed
                customer.save()
                messages.success(request, 'Payment done successful')
                return redirect('payment')
            else:
                messages.error(request, 'Sorry you dont have enough money to pay such amount')
                return redirect('payment')
        else:
            messages.error(request, 'Meter number not exist')
            return redirect('payment')

    return render(request, 'payment.html')


def notification(request):
    notifications = Notification.objects.all()
    return render(request, 'notification.html', {'context': notifications})

def payment_history(request):
    history = PaymentHistory.objects.all()
    return render(request, 'payment_history.html', {'context': history})