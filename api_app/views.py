from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Request, Device
from .models import RequestSerializer
import requests

# Useful variables
phone_number = '+255-----'
message_to_send = 'mesage comes here'
api_key = 'textbelt api key'

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

        # Sending SMS request
        req = requests.post('https://textbelt.com/text',{
            'phone': phone_number,
            'message': message_to_send,
            'key': api_key,
        })
        print(req.json())
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
        serializer = RequestSerializer(device_request, data=response_data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS', status=status.HTTP_202_ACCEPTED)
        else:
            return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Request('Device not registered', status=status.HTTP_404_NOT_FOUND)