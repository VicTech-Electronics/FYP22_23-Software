from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import InfoSerializer
from twilio.rest import Client


# Twillio sms credentials
account_sid = 'AC272eb7b173b88e71f4df1a34e788c52f'
auth_token = '683809024cc03125653bad91cd2b4355'
client = Client(account_sid, auth_token)
twilio_phone = '+15734982063'
client_phone = '+255719482668'

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
            'description': 'View documentation for this API'
        },
        {
            'endpoint': '.../api/info',
            'method': 'POST',
            'body': '{"vehicle_number": str, "latitude": float, "longitude": float, "description": str}',
            'description': 'Adding new accident information',
        }
    ]
    return Response(info, status=status.HTTP_200_OK)


@api_view(['POST'])
def informations(request):
    vehicle_number = request.data.get('vehicle_number')
    serializer = InfoSerializer(data = request.data)

    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    description = request.data.get('description')

    sms_to_send = f'INFORMATION: \nAccident detected at: \nLatitude: {latitude}, \nLongitude: {longitude}, Descriptions: {description}. \nLink: https://tute-fyp22-23-c169130615c7.herokuapp.com'
    sms_response = sendSMS(sms_to_send)
    print(f"Message sent! SID: {sms_response}")


    if serializer.is_valid():
        serializer.save()
        return Response('[SUCCESS]')
    else:
        return Response('[FAIL]', status=status.HTTP_400_BAD_REQUEST)