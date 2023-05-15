from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@unauthenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account', detail='reports')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

@unauthenticated
def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def account(request, **kwarg):
    no_of_reports = Report.objects.count()
    no_of_calls = Call.objects.count()
    no_of_messages = Message.objects.count()
    detail = kwarg.get('detail')

    if detail=='reports':
        data = 'Reports'
        values = Report.objects.all()
    elif detail=='calls':
        data = 'Calls'
        values = Call.objects.all()
    elif detail=='messages':
        data = 'Messages'
        values = Message.objects.all()

    return render(request, 'account.html', {
        'data': data,
        'values': values,
        'no_of_reports': no_of_reports,
        'no_of_calls': no_of_calls,
        'no_of_messages': no_of_messages,
    })
