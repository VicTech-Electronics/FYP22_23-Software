from .models import CaseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_management.models import Driver
from rest_framework import status
from twilio.rest import Client
import requests



# Twillio sms credentials
account_sid = 'AC272eb7b173b88e71f4df1a34e788c52f'
auth_token = '683809024cc03125653bad91cd2b4355'
client = Client(account_sid, auth_token)
twilio_phone = '+15734982063'
client_phone = '+255678401013'

# Metho to send sms
def sendSMS(sms):
    message = client.messages.create(
        body=sms,
        from_=twilio_phone,
        to=client_phone
    )
    return message.sid


@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpoint': '.../api',
            'method': 'GET',
            'body': None,
            'description': 'View the documentation for this API'
        },
        {
            'endpoint': '.../api/create',
            'method': 'POST',
            'body': '{"vehicle_number": str, "latitude": float, "longitude": float}',
            'decription': 'Adding a new case'
        }
    ]
    return Response(info, status=status.HTTP_200_OK)



@api_view(['POST'])
def addCase(request):
    # Data to post from the accident scene
    vehicle_number = request.data.get('vehicle_number')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if Driver.objects.filter(vehicle_number=vehicle_number).exists():
        driver = Driver.objects.get(vehicle_number=vehicle_number)
        case_data = {
            'driver': driver.pk,
            'latitude': latitude,
            'longitude': longitude,
        }
    else:
        return Response('Vehicle number not exists', status=status.HTTP_404_NOT_FOUND)

    serializer = CaseSerializer(data=case_data)
    if serializer.is_valid():
        driver_name = driver.username
        message = f'Hello! {driver_name}. \nPhone use while driving is detected by the system. \nFine cost is Tsh.20,000/='

        sms_respose = sendSMS(message)
        print(f'Message sent SID: {sms_respose}')

        serializer.save()
        return Response('SUCCESS')
    else:
        return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)