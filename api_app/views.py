from rest_framework import status
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main_app.models import *

# Create your views here.
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
            'endpoint': '.../api/check',
            'method': 'POST',
            'body': '{"type": str, "number": str}',
            'description': 'Check the existance of the number',
        }
    ]
    return Response(info, status=status.HTTP_200_OK)


@api_view(['POST'])
def check(request):
    type = request.data.get('type')
    number = request.data.get('number')

    if type == 'plate':
        Database = PlateNumber
    elif type == 'card':
        Database = CardNumber

    if Database.objects.filter(number=number).exists():
        return Response('exist', status=status.HTTP_302_FOUND)
    else:
        return Response('not exist', status=status.HTTP_404_NOT_FOUND)