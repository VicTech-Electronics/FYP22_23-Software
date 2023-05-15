from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import InfoSerializer

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
    if serializer.is_valid():
        serializer.save()
        return Response('SUCCESS')
    else:
        return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)