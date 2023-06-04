from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main_app.models import BreakerState
from .serializers import BreakerStateSerializer

# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpont': '.../api',
            'method': 'GET',
            'body': None,
            'descriptions': 'View this API documentations'
        },

        {
            'endpoint': '.../api/get',
            'method': 'GET',
            'body': None,
            'descriptions': 'Get breaker state value'
        }
    ]

    return Response(info, status=status.HTTP_200_OK)


@api_view(['GET'])
def getData(request):
    data = BreakerState.objects.get(id=1)
    serializer = BreakerStateSerializer(data)
    return Response(serializer.data)
