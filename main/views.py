from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import admin_only, unauthorized_user

# Create your views here.
@login_required(login_url='login')
@admin_only
def admin(request):
    sales = 0
    revenue = 0
    no_of_costomers = 0
    
    customers = Customer.objects.all()
    transactions = Transaction.objects.all()

    customer_status = []
    for customer in customers:
        no_of_costomers += 1

        if customer.status:
            customer_status.append("Active")
        else:
            customer_status.append("Blocked")

    for transaction in transactions:
        sales += 1
        revenue += transaction.amount

    for customer, status in zip(customers, customer_status):
        customer.status = status

    context = {
        'no_of_customers': no_of_costomers,
        'sales': sales,
        'revenue': revenue,
    }
    return render(request, 'admin.html', {'data': context, 'customers': customers})


@login_required(login_url='login')
def home(request, pk):
    group = request.user.groups.first().name
    customer = Customer.objects.get(pk=pk) 
    transactions = Transaction.objects.filter(customer = customer.pk)
    return render(request, 'home.html', {'user_group': group, 'customer': customer, 'transactions': transactions})

@unauthorized_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:  
        return render(request, 'login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        card_no = request.POST.get('card_no')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username alread exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                customer = Customer.objects.create(user=user, card_no=card_no, amount=0.0, status=False)
                user.save()
                customer.save()

                group = Group.objects.get(name='customer')
                user.groups.add(group)

                messages.success(request, 'Account registered successfull')
                return redirect('login')
            
        else:
            messages.error(request, 'Password mismatch')
            return redirect('register')
    else:
        print('Method is not POST')
        return render(request, 'register.html')

@login_required(login_url='login')
def permition(request, id): 
    customer = Customer.objects.get(pk = id)
    user = User.objects.get(username=customer.user.username)

    permision = request.POST.get('permision')
    
    if permision ==  'activate':
        customer.status = True
        customer.save()
    elif permision == 'block':
        customer.status = False
        customer.save()
    elif permision == 'delete':
        customer.delete()
        user.delete()

    return redirect('../')

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        users = User.objects.filter(username = name)
        if Customer.objects.filter(user__in = users).exists():
            sales = 0
            revenue = 0
            no_of_costomers = 0

            customers = Customer.objects.all()
            transactions = Transaction.objects.all()

            for transaction in transactions:
                sales += 1
                revenue += transaction.amount
            
            
            for _ in customers:
                no_of_costomers += 1
                

            context = {
                'no_of_customers': no_of_costomers,
                'sales': sales,
                'revenue': revenue,
            }
            
            customers = Customer.objects.filter(user__in = users)

            customers_status = []
            for customer in customers:
                if customer.status:
                    customers_status.append("Active")
                else:
                    customers_status.append("Blocked")

            for customer, status in zip(customers, customers_status):
                customer.status = status

            return render(request, 'admin.html', {'data': context, 'customers': customers})
        else:
            messages.info(request, f'User with a name {name} not exists')
            return redirect('../')
    else:
        return redirect('../')