import random
import string
from fpdf import FPDF
from .classes import PDF
from django.http import HttpResponse
from .models import Patient, Medical
from datetime import date, timedelta

# Function to calculate the age of the patient
def patient_age(patient):
    # Calculate the age of the patient
    time = date.today() - patient.date_of_birth
    patient_age = int(time.days / 365.25)
    return patient_age

# Function to generate uniq CODE
def generate_code():
    code_length = 10
    code_characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(code_characters) for _ in range(code_length))
    return code

# Function to generate code PDF
def generate_code_PDF(request, code):
    # Get the required informations
    patient = Patient.objects.get(code=code)

    # Generate the PDF
    pdf = FPDF(orientation='portrait', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font(family='times', style='B', size=24)
    pdf.cell(0, 0, code)

    # Output the PDF
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f"attachment; filename={patient.surname}.pdf"
    return response

# Function to generate medical_advice PDF
def generate_treatment_advice_PDF(request, code, advice):
    # Get the required fields
    patient = Patient.objects.get(code=code)
    medical = Medical.objects.get(patient=patient)
    age = patient_age(patient)
    
    # Generate the PDF
    pdf = PDF(orientation='portrait', unit='mm', format='letter')
    
    # personal Informations
    # Heading
    pdf.add_page()
    pdf.set_text_color(55, 121, 186)
    pdf.set_font('times', 'BU', 16)
    pdf.cell(0, 10, 'Personal Informations:', ln=True)
    # Fullname
    pdf.set_x(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', 'B', 12)
    pdf.cell(30, 5, 'Full name:')
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{patient.surname}, {patient.first_name} {patient.middle_name}', ln=True)
    # Blood group
    pdf.set_x(20)
    pdf.set_font('times', 'B', 12)
    pdf.cell(30, 5, 'Blood group:')
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{patient.blood_group}', ln=True)
    # Age
    pdf.set_x(20)
    pdf.set_font('times', 'B', 12)
    pdf.cell(30, 5, 'Age:')
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{age}', ln=True)
    # Gender
    pdf.set_x(20)
    pdf.set_font('times', 'B', 12)
    pdf.cell(30, 5, 'Gender:')
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{patient.gender}', ln=True)
    pdf.ln(5)


    # Medical examinations  
    pdf.set_text_color(55, 121, 186)
    pdf.set_font('times', 'BU', 16)
    pdf.cell(0, 10, 'Medical Examinations:', ln=True)
    # Examinations
    pdf.set_x(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{medical.medical_examination}', ln=True)
    pdf.ln(5)

    # Medical advice  
    pdf.set_text_color(55, 121, 186)
    pdf.set_font('times', 'BU', 16)
    pdf.cell(0, 10, 'Medical advice:', ln=True)
    # Examinations
    pdf.set_x(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('times', '', 12)
    pdf.cell(0, 5, f'{advice}', ln=True)
    pdf.ln(5)

    # Output the PDF
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f"attachment; filename={patient.surname}.pdf"
    return response