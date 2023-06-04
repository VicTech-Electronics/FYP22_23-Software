from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .functions import generate_code, patient_age
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *

# Create your views here.
@unauthenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        
    return render (request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


# Home page view for Patient registration
@login_required(login_url='login')
@nurse_only
def home(request):
    if request.method == 'POST':
        # Personal informations
        surname = request.POST.get('surname')
        middle_name = request.POST.get('middle_name')
        first_name = request.POST.get('first_name')
        patient_id = request.POST.get('patient_id')
        religion = request.POST.get('religion')
        date_of_birth = request.POST.get('birth_date')
        mobile = request.POST.get('mobile')
        blood_group = request.POST.get('blood_group')
        gender = request.POST.get('gender')

        # Residential informations
        region = request.POST.get('region')
        district = request.POST.get('district')
        ward = request.POST.get('ward')

        #  Generate uniq code
        code = generate_code()
        while Patient.objects.filter(code=code).exists():
            code = generate_code()

        # Checking option
        first_time = request.POST.get('first_time')

        if first_time:
            if Patient.objects.filter(patient_id=patient_id).exists():
                messages.error(request, f'Patient ID {patient_id}, alread in use')
                return redirect('home')

            # Create patient
            patient = Patient.objects.create(
                surname = surname,
                middle_name = middle_name,
                first_name = first_name,
                patient_id = patient_id,
                religion = religion,
                date_of_birth = date_of_birth,
                mobile = mobile,
                blood_group = blood_group,
                gender = gender,
                region = region, 
                district = district,
                ward = ward,
                code = code
            )
            patient.save()  
        else:
            try:
                patient = Patient.objects.get(patient_id=patient_id)
            except Patient.DoesNotExist:
                messages.error(request, f'Patient of ID {patient_id}, Does not exist')
                return redirect('home')
            
            patient.code = code
            patient.save()

        #  Return the page with the download link
        return render(request, 'registration.html', {'pdf_code': code})

    return render (request, 'registration.html')


# Report view for viewing Patient report for medical advice after examinations
@login_required(login_url='login')
@doctor_only
def report(request):
    new = Medical.objects.filter(completed=False)
    all = Medical.objects.all()
    return render(request, 'report.html', {'new_reports': new, 'all_reports': all})

# Report view for Doctor medical advice
@login_required(login_url='login')
@doctor_only
def doctor(request, report):
    patient = Patient.objects.get(code=report)
    medical = Medical.objects.get(patient=patient)
    age = patient_age(patient)

    if request.method == 'POST':
        # Get doctor advice from the page
        advice = request.POST.get('doctor_report')

        # Modify the medical report by adding the Treatment advice
        medical.treatment_advice = advice
        medical.completed = True
        medical.save()

        context = {
            'patient': patient,
            'code': report,
            'medical': medical,
            'treatment': advice,
            'patient_age': age
        }

        return render(request, 'doctor.html', {'context': context})
    
    context = {
        'patient': patient,
        'code': report,
        'medical': medical,
        'patient_age': age
    }

    return render (request, 'doctor.html', {'context': context})