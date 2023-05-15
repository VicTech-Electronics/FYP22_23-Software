from rest_framework.response import Response
from rest_framework import status
from .models import RequestSerializer
from main_app.models import Request, Device
from rest_framework.decorators import api_view

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

    current_data = Request.objects.get(pk = device.pk)
    updated_data = {
        'device': device.pk,
        'latitude': request.data.get('latitude'),
        'longitude': request.data.get('longitude'),
        'heart_rate': request.data.get('heart_rate'),
        'body_temperature': request.data.get('body_temp'),
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