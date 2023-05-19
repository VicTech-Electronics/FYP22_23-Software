from .models import CaseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_management.models import Driver
from rest_framework import status
import requests

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
        phone_number = driver.contact
        message = f'Hello {driver_name}. \n System detect you are using phone while Driving, Fine cost is Tsh.20000/='
        sms_api_key = 'textbelt api key comes here'

        # sms_response = requests.post('https://textbelt.com/text',{
        #     'phone': phone_number,
        #     'message': message,
        #     'key': sms_api_key
        # })
        # print(sms_response.json)

        serializer.save()
        return Response('SUCCESS')
    else:
        return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)