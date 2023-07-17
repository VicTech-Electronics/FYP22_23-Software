from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from main_app.models import Patient, Medical

# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpoint': '.../api',
            'methode': 'GET',
            'body': None,
            'description': 'View the documentation to this API'
        },
        {
            'endpoint': '.../api/examine',
            'methode': 'POST',
            'body': '{"code": str, "examination": str}',
            'description': 'Post the medical examination report to the server'
        }
    ]

    return Response(info, status=status.HTTP_200_OK)


@api_view(['POST'])
def examine(request):
    # Collect posted data
    code = request.data.get('code')
    examination = request.data.get('examination')

    try:
        patient = Patient.objects.get(code=code)
    except Patient.DoesNotExist:
        return Response(f'Patient of code {code}, not exist', status=status.HTTP_404_NOT_FOUND)
    
    medical = Medical.objects.create(patient=patient, medical_examination=examination)
    medical.save()

    return Response('SUCCESS', status=status.HTTP_200_OK)