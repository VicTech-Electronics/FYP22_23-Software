from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Request, Device
from .models import RequestSerializer
from twilio.rest import Client
import requests

# Twillio sms credentials
account_sid = 'AC272eb7b173b88e71f4df1a34e788c52f'
auth_token = '683809024cc03125653bad91cd2b4355'
client = Client(account_sid, auth_token)
twilio_phone = '+15734982063'
client_phone = '+255625961607'

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
            'endpoint': '/api/request',
            'method': 'POST',
            'body': '{"device": "#"}',
            'description': 'Make a request by sending the device ID to # in a body'
        },

        {
            'endpoint': '/api/response',
            'method': 'PUT',
            'body': '{"device": "#"}',
            'description': 'Make a response by sending the response device ID to # in a body'
        }
    ]

    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def req_endpoint(request):
    device_id = Device.objects.get(device_id=request.data.get('device'))
    
    if device_id is not None:
        req_data = Request.objects.create(
            device = device_id
        )
        req_data.save()
        
        bed_number = str(device_id.bed_number)
        ward_name = str(device_id.ward_name)

        sms_to_send = f'INFORMATION: \nPatient need emergence care \nWard name: {ward_name}, \nBed number: {bed_number}, \nPlease take quick action'
        sms_response = sendSMS(sms_to_send)
        print(f'Message send SID: {sms_response}')

        return Response('SUCCESS', status=status.HTTP_202_ACCEPTED)
    else:
        return Response('Device not registered', status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def resp_endpoint(request):
    device_id = Device.objects.get(device_id=request.data.get('device'))
    print(f'Data req: {request.data}')

    if device_id is not None:
        device_request = Request.objects.get(device=device_id)
        response_data = {
            'device': device_id.pk
        }

        bed_number = str(device_id.bed_number)
        ward_name = str(device_id.ward_name)
        
        sms_to_send = f'INFORMATION: \nRequest attended \nWard name: {ward_name}, \nBed number: {bed_number}'
        sms_response = sendSMS(sms_to_send)
        print(f'Message send SID: {sms_response}')

        serializer = RequestSerializer(device_request, data=response_data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS', status=status.HTTP_202_ACCEPTED)
        else:
            return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Request('Device not registered', status=status.HTTP_404_NOT_FOUND)