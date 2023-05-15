from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .decorators import *
from django.utils import timezone
import datetime

# Create your views here.
@login_required(login_url='login')
# @admin_only
def home(request):
    total_nurses = 0
    total_request = 0
    total_response = 0
    available_nurses = 0
    percentage_response = 0

    ward_names = []
    bed_numbers = []
    request_times = []
    response_times = []
    response_status = []
    patient_request = []
    nurse_name = []
    nurse_contact = []
    time_in = []
    nurse_attendence = []

    # Time decralation
    now = timezone.now()
    date = now.date()
    day = timezone.now().weekday()
    date_to_pass = timezone.make_aware(
        datetime.datetime(now.year, now.month, now.day - 1)
    )

    # Decralation of days of the week
    if day == 0: weekday = 'Monday'
    elif day == 1: weekday = 'Tuesday'
    elif day == 2: weekday = 'Wednesday'
    elif day == 3: weekday = 'Thursday'
    elif day == 4: weekday = 'Friday'
    elif day == 5: weekday = 'Saturday'
    elif day == 6: weekday = 'Sunday'

    # Query attendence
    attendence = Attendence.objects.filter(time_in__gte = date_to_pass)
    for attend in attendence:
        available_nurses += 1

        nurse_id = attend.nurse.pk
        nurse = Nurse.objects.get(pk=nurse_id)
        nurse_name.append(nurse.user.username)
        nurse_contact.append(nurse.contacts)
        time_in.append(attend.time_in)

    # Query timetable
    today = WeekDay.objects.get(day=weekday)
    time_table = TimeTable.objects.get(day=today.pk)
    for _ in time_table.nurse.all():
        total_nurses += 1

    # Query request
    today_requests = Request.objects.filter(request_time__gte = date_to_pass)
    for req in today_requests:
        request_times.append(req.request_time)

        if req.responded():
            response_times.append(None)
            response_status.append('pending')
        else:
            response_times.append(req.response_time)
            response_status.append('responded')
            total_response += 1
            
        total_request += 1
        percentage_response = round((total_response / total_request) * 100, 2)

    requested_device = Request.objects.values('device')
    requested_device = Device.objects.filter(pk__in=requested_device)
    for device in requested_device:
        ward_names.append(device.ward_name)
        bed_numbers.append(device.bed_number)

    # Today details context
    today_details = {
        'date': date,
        'available_nurses': available_nurses,
        'total_nurses': total_nurses,
        'total_request': total_request,
        'percentage_response': percentage_response,
    }

    # Patient requests context
    for ward, bed, req_t, res_t, status in zip(ward_names, bed_numbers, request_times, response_times, response_status):
        data = {
            'ward_name': ward,
            'bed_number': bed,
            'request_time': req_t,
            'response_time': res_t,
            'response_status': status,
        }
        patient_request.append(data)

    # Nurse attendence context
    for name, contact, t_in in zip(nurse_name, nurse_contact, time_in):
        data = {
            'nurse_name': name,
            'nurse_contacts': contact,
            'time_in': t_in,
        }  
        nurse_attendence.append(data)


    # context to pass
    context = {
        'today_details': today_details,
        'patient_request': patient_request,
        'nurse_attendence': nurse_attendence,
    }

    return render(request, 'home.html', {'context': context})

@unauthenticated
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            _user = User.objects.get(username=username)
            group = _user.groups.first().name

            if group == 'nurse':
                nurse = Nurse.objects.get(user = _user.pk)
                attendence = Attendence.objects.create(nurse = nurse)
                attendence.save()
                messages.success(request, f'Hello {request.user}, Your data are submited successull')
                logout(request)
                return redirect('login')
            else:
                messages.success(request, f'Hello {request.user}, Login successfuly')
                return redirect('home')
                
        else:
            messages.error(request, 'Invalid credentials')  
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.info(request, 'Loged out')
    return redirect('login')


@login_required(login_url='login')
# @admin_only
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username alread exist')
                return redirect('registration')
            else:
                user =  User.objects.create_user(username=username, password=password1)
                nurse = Nurse.objects.create(user=user, contacts=contact)
                user.save()
                nurse.save()

                group = Group.objects.get(name='nurse')
                user.groups.add(group)

                messages.success(request, f'{username}, Registered successfuly')
                return redirect('registration')
        else:
            messages.error(request, 'Passwords mismatch')
            return redirect('registration')
    else:
        return render(request, 'register.html')

# @admin_only
def device_registration(request):
    if request.method == 'POST':
        device_number = request.POST.get('device_number')
        ward_name = request.POST.get('ward_name')
        bed_number = request.POST.get('bed_number')

        if Device.objects.filter(device_id=device_number).exists():
            messages.info(request, 'Device number alread exist')
            return redirect('device_reg')
        else:
            device = Device.objects.create(device_id=device_number, ward_name=ward_name, bed_number=bed_number)
            device.save()

            messages.success(request, f'Device {device_number}, registered successfuly')
            return redirect('device_reg')
    else:
        return render(request, 'device_reg.html')