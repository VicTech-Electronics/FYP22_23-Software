from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from .models import RequestSerializer
from main_app.models import Request, Device
from rest_framework.decorators import api_view


# Twillio sms credentials
account_sid = 'AC272eb7b173b88e71f4df1a34e788c52f'
auth_token = '683809024cc03125653bad91cd2b4355'
client = Client(account_sid, auth_token)
twilio_phone = '+15734982063'
client_phone = '+255712818281'

min_rate = 60.0
max_rate = 120.0
min_temp = 36.5
max_temp = 37.5

# Metho to send sms
def sendSMS(sms):
    message = client.messages.create(
        body=sms,
        from_=twilio_phone,
        to=client_phone
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
            'description': 'View documentation on how to use this API'
        },
        {
            'endpoint': '.../api/add',
            'method': 'POST',
            'body': '{"device_number": str, "latitude": float, "longitude": float, "heart_rate": float, "body_temp": float}',
            'description': 'Add new infomation request for device status',
        },
        {
            'endpoint': '.../api/update/',
            'method': 'PUT',
            'body': '{"device_number": str, "latitude": float, "longitude": float, "heart_rate": float, "body_temp": float}',
            'description': 'Send device infomations to update device status',
        },
        {
            'endpont': '.../api/delete/',
            'method': 'DELETE',
            'body': '{"device_number": str}',
            'description': 'Delete device field data'
        }
    ]
    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def addInfo(request):
    device_number = request.data.get('device_number')
    if Device.objects.filter(device_number = device_number).exists():
        device = Device.objects.get(device_number = device_number)
        if Request.objects.filter(device = device.pk).exists():
            return Response('Sorry, Request alread exist', status=status.HTTP_400_BAD_REQUEST)
        else:
            post_data = {
                'device': device.pk,
                'latitude': request.data.get('latitude'),
                'longitude': request.data.get('longitude'),
                'heart_rate': request.data.get('heart_rate'),
                'body_temperature': request.data.get('body_temp'),
            }

            serializer = RequestSerializer(data = post_data)
            if serializer.is_valid():
                serializer.save()
                return Response('SUCCESS')
            else:
                return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response ('Sorry device not exist', status=status.HTTP_400_BAD_REQUEST)

    


@api_view(['PUT'])
def updateInfo(request):
    device = Device.objects.get(device_number = request.data.get('device_number'))

    heart_rate = float(f"{request.data.get('heart_rate'): .2f}")
    body_temperature = float(f"{(request.data.get('body_temp') + 6): .2f}")

    if heart_rate < min_rate or heart_rate > max_rate or body_temperature < min_temp or body_temperature > max_temp:
        sms_to_send = f'WARNING: \nEmergence condition \nHeart rate: {heart_rate} \nBody temperature: {body_temperature} \nLink: htts://spona-fyp22-23.herokuapp.com'
        sms_response = sendSMS(sms_to_send)
        print(f"Message sent! SID: {sms_response}")

    current_data = Request.objects.get(pk = device.pk)
    updated_data = {
        'device': device.pk,
        'latitude': request.data.get('latitude'),
        'longitude': request.data.get('longitude'),
        'heart_rate': heart_rate,
        'body_temperature': body_temperature
    }

    serializer = RequestSerializer(current_data, data=updated_data)
    if serializer.is_valid():
        serializer.save()
        return Response('SUCCESS')
    else:
        return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteInfo(request, device_num):
    device = Device.objects.get(device_number = device_num)
    data = Request.objects.get(pk = device.pk)
    data.delete()
    return Response('DELETED')