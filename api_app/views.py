from rest_framework import status
from django.shortcuts import redirect
from .models import IndicatorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from geopy.distance import geodesic
from twilio.rest import Client
from main_app.models import *

# Twillio sms credentials
account_sid = 'AC272eb7b173b88e71f4df1a34e788c52f'
auth_token = '683809024cc03125653bad91cd2b4355'
client = Client(account_sid, auth_token)
twilio_phone = '+15734982063'

# Metho to send sms
def sendSMS(sms, phone):
    message = client.messages.create(
        body=sms,
        from_=twilio_phone,
        to=phone
    )
    return message.sid

# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpoint': '.../api',
            'method': 'GET',
            'body': None,
            'description': 'View documentation for this API',
        },
        {
            'endpoint': '.../api/create',
            'method': 'POST',
            'body': '{"vehicle": str, "flame": float, "smoke": float, "vibration": float, "gyroscope": float, "latitude": float, "longitude": float, "brake": boolean}',
            'description': 'Post the accident indicator information',
        },
        {
            'endpoint': '.../api/confirm',
            'method': 'POST',
            'body': '{"vehicle": str, "latitude": float, "longitude": float}',
            'description': 'Confirm the existance of accident',
        },
        {
            'endpoint': '.../api/cancel/<str:vehicle_number>',
            'methode': 'DELETE',
            'body': None,
            'description': 'Cancel the accident information',
        }
    ]
    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def create(request):
    vehicle_number = request.data.get('vehicle')

    if Vehicle.objects.filter(vehicle_number = vehicle_number).exists():
        vehicle = Vehicle.objects.get(vehicle_number = vehicle_number)
    else:
        return Response('Vehicle not registered', status=status.HTTP_404_NOT_FOUND)

    request.data['vehicle'] = vehicle.pk
    serializer = IndicatorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print('Indicator saved')
        return redirect('classifier', vehicle.pk)
    else:
        return Response('[FAIL]', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm(request):
    # Variable to store data for Accident Information after being detected
    distances = []
    hospital_locations = []
    accident_point = (
        request.data.get('latitude'), 
        request.data.get('longitude')
    )

    # Calculation of Distance from all hospital location to the accident seen
    hospitals = Hospital.objects.all()
    for hospital in hospitals:
        hospital_point = (
            hospital.latitude, 
            hospital.longitude
        )
        distance = geodesic(accident_point, hospital_point).km
        
        distances.append(distance)
        hospital_locations.append(hospital_point)
    
    # Extract data obtained from the calculation above
    short_distance = min(distances)
    index = distances.index(short_distance)
    hospital_location = hospital_locations[index]
    

    # Extract data for accident infomation
    if Vehicle.objects.filter(vehicle_number = request.data.get('vehicle')).exists():
        vehicle = Vehicle.objects.get(vehicle_number = request.data.get('vehicle'))
        target_hospital = Hospital.objects.get(
            latitude = hospital_location[0],
            longitude = hospital_location[1]
        )
    else:
        return Response('[Vehicle not registered]', status=status.HTTP_404_NOT_FOUND)

    # Create accident infomation
    accident = Accident.objects.create(
        vehicle = vehicle,
        hospital = target_hospital,
        confidence = 100.0,
        latitude = request.data.get('latitude'),
        longitude = request.data.get('longitude'),
    )

    # Sending sms to the relatives of the vehicle users
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    sms_to_send = f'Accident detected for vehicle No: {vehicle.vehicle_number}, \nAccident location: \nLatitude: {latitude}, \nLongitude: {longitude}, \nLink: https://victonix-fyp.herokuapp.com \nInformation about the accident sent to {hospital.user.username}. Please take the action to help rescue activities'
    sms_response = sendSMS(sms_to_send, vehicle.phone1)
    print(f'Message send SID: {sms_response}')
    sms_response = sendSMS(sms_to_send, vehicle.phone2)
    print(f'Message send SID: {sms_response}')

    accident.save()
    return Response('[SUCCESS]')


@api_view(['DELETE'])
def cancel(request, vehicle_number):
    if Vehicle.objects.filter(vehicle_number = vehicle_number).exists():
        vehicle = Vehicle.objects.get(vehicle_number = vehicle_number)
        if Accident.objects.filter(vehicle = vehicle.pk).exists():
            accident = Accident.objects.get(vehicle = vehicle.pk, status=False)
            accident.delete()
            return Response('[CANCELED]', status=status.HTTP_202_ACCEPTED)
        else:
            return Response('[No accident record for such a vehicle]', status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('[Vehicle not registered]', status=status.HTTP_404_NOT_FOUND)