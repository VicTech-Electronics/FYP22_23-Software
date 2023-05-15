from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from main_app.models import Device
from .models import *

# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        
        {
            'endpoint': '.../api',
            'method': 'GET',
            'body': None,
            'descriptions': 'View the documentation for this API'
        },
        {
            'endpoint': '.../api/report',
            'method': 'POST',
            'body': '{"device": str, "title": str, "content": str, "latitude": float, "longitude": float}',
            'descriptions': 'Sending the report to this site'
        },
        {
            'endpoint': '.../api/call',
            'method': 'POST',
            'body': '{"device": str, "phone": int, "response": boolean}',
            'descriptions': 'Sending phone call status infomations to this site'
        },
        {
            'endpoint': '.../api/message',
            'method': 'POST',
            'body': '{"device": str, "phone": int, "content": str}',
            'descriptions': 'Sending message infomation to this site'
        },

        "NOTE: Start phone number with neigher 0 nor +255, eg: 744952269",
    ]
    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def report(request):
    if Device.objects.filter(device_id = request.data.get('device')).exists():
        request.data['device'] = Device.objects.get(device_id = request.data.get('device')).pk

        serializer = ReportSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS')
        else:
            return Response('FAIL')
    else:
        return Response('Device not exist', status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def call(request):
    if Device.objects.filter(device_id = request.data.get('device')).exists():
        request.data['device'] = Device.objects.get(device_id = request.data.get('device')).pk

        serializer = CallSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS')
        else:
            return Response('FAIL')
    else:
        return Response('Device not exist', status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def message(request):
    if Device.objects.filter(device_id = request.data.get('device')).exists():
        request.data['device'] = Device.objects.get(device_id = request.data.get('device')).pk
       
        serializer = MessageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS')
        else:
            return Response('FAIL')
    else:
        return Response('Device not exist', status=status.HTTP_404_NOT_FOUND)