from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Personnel(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class Patient(models.Model):
    # Personal informations
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patient_id = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    religion = models.CharField(
        max_length= 10,
        choices=[
            ('empty', ''),
            ('christian', 'Christian'),
            ('islamic', 'Islamic'),
            ('other', 'Other')
        ],
        default= 'empty',
    )
    blood_group = models.CharField(
        max_length= 10,
        choices=[
            ('empty', ''),
            ('Group A', 'Group A'),
            ('Group B', 'Group B'),
            ('Group AB', 'Group AB'),
            ('Group O', 'Group O'),
        ],
        default= 'empty',
    )
    gender = models.CharField(
        max_length= 10,
        choices=[
            ('empty', ''),
            ('Male', 'Male'),
            ('Female', 'Female')
        ],
        default= 'empty',
    )

    # Residential informations
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)

    # Identification code
    code = models.CharField(max_length=10)


    def __str__(self):
        return self.surname
    

class Medical(models.Model):
    patient = models.ForeignKey(Patient, null=False, on_delete=models.CASCADE)
    medical_examination = models.CharField(max_length=500)
    treatment_advice = models.TextField(default='Error: Miss treatment advice from the Doctor')
    completed = models.BooleanField(
        default=False,
        choices=[
            (False, 'Pending'),
            (True, 'Done')
        ]
    )

    def __str__(self):
        return self.patient.code
