from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main_app.models import Customer, Expenses, Transaction
from .decorators import unauthenticated
from django.contrib.auth.models import User
from django.db.models import Q
import json

# Create your views here.
@login_required(login_url='login')
def home(request):
    # Count costomers from the model
    no_of_customers = Customer.objects.all().count()

    # Count revenue from the model
    revenue = 0
    for transaction in Transaction.objects.all():
        revenue = revenue + transaction.amount

    # Count expenses from the model
    expenses = 0
    for info in Expenses.objects.all():
        expenses = expenses + info.amount

    # Calculate profit from revenue and expenses counted above
    profit = revenue - expenses

    # Calculate monthly revenue
    monthly_income = 0
    monthly_revenue = []
    for month in range(1, 13):
        for rev in Transaction.objects.filter(date_time__month=month):
            monthly_income = monthly_income + rev.amount
        monthly_revenue.append(monthly_income)
        monthly_income = 0
    
    # Calculate monthly expenses
    monthly_outcome = 0
    monthly_expenses = []
    for month in range(1, 13):
        for expens in Expenses.objects.filter(date_time__month=month):
            monthly_outcome = monthly_outcome + expens.amount
        monthly_expenses.append(monthly_outcome)
        monthly_outcome = 0
    
    # Collect data for no_of_customer, revenue, expenses and profit
    data = {
        'no_of_customers': no_of_customers,
        'revenue': revenue,
        'expenses': expenses,
        'profit': profit
    }

    # Collect monthly data for revenue and expenses
    transactions = {
        'revenue': monthly_revenue,
        'expenses': monthly_expenses,
    }


    # Calculate the service demand over the year
    demands = []
    for month in range(1, 13):
        urination = 0
        defecation = 0
        shower = 0
        for _ in Transaction.objects.filter(date_time__month=month):
            urination = Transaction.objects.filter(Q(date_time__month=month) & Q(details='urination')).count()
            defecation = Transaction.objects.filter(Q(date_time__month=month) & Q(details='defecation')).count()
            shower = Transaction.objects.filter(Q(date_time__month=month) & Q(details='shower')).count()
        
        demands.append(
            {
                month: {
                    'urination': urination,
                    'defecation': defecation,
                    'shower': shower
                }
            }
        )
    
    # Collect all required informations
    informations = {
        'transactions': json.dumps(transactions),
        'demands': json.dumps(demands),
    }
    
    print(f"Data: {informations['demands']}")
    return render(request, 'index.html', {'data': data, 'informations': informations})

@unauthenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Hello {username}, you are successfull login')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        card_number = request.POST.get('card_number')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username alread exist')
            return redirect('register')
        
        if Customer.objects.filter(card_number=card_number).exists():
            messages.error(request, 'Card alread in use')
            return redirect('register')

        if password == password_confirm:
            user = User.objects.create(username=username, password=password)
            user.save()
            customer = Customer.objects.create(user=user, card_number=card_number)
            customer.save()
            messages.success(request, f'{username}, Registered successful')
            return redirect('register')
        else:
            messages.error(request, 'Password missmatch')
            return redirect('register')

    return render(request, 'register.html')