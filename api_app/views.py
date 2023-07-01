from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NotificationSerializer
from main_app.models import Customer
from .models import Notification
from rest_framework import status
import requests

# Create your views here.
# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpoint': '.../api',
            'method': 'GET',
            'body': None,
            'description': 'Show documentation of this API'
        },
        {
            'endpoint': '.../api/usage',
            'method': 'POST',
            'body': '{"device": str, "units": float}',
            'description': 'Make a request by sending the amount of units used currently'
        },

        {
            'endpoint': '.../api/notification',
            'method': 'POST',
            'body': '{"customer": str, "title": str, "detail": str}',
            'description': 'Make a request to send the device notifications'
        }
    ]

    return Response(info, status=status.HTTP_200_OK)


@api_view(['POST'])
def usage(request):
    if Customer.objects.filter(meter_number=request.data.get('device')).exists():
        customer = Customer.objects.get(meter_number=request.data.get('device'))
        remaining_units = customer.units - request.data.get('units')
        if remaining_units < 0.0:
            remaining_units = 0.0
        customer.units = remaining_units
        customer.save()
        return Response(remaining_units)
    else:
        return Response('Meter number not registered', status=status.HTTP_404_NOT_FOUND)

        
@api_view(['POST'])
def notification(request):
    if Customer.objects.filter(meter_number=request.data.get('customer')).exists():
        customer = Customer.objects.get(meter_number=request.data.get('customer'))
        request.data['customer'] = customer.pk

        print(f'Data: {request.data}')

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('SUCCESS')
        else:
            return Response('FAIL')
    else:
        return Response('Meter number not registered', status=status.HTTP_404_NOT_FOUND)