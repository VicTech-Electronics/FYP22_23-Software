from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main_app.models import Customer
from .models import TransactionSerializer

# Create your views here.
@api_view(['GET'])
def documentation(request):
    info = [
        {
            'endpoint': '.../api',
            'methode': 'GET',
            'body': None,
            'description': 'View the documentation for this API'
        },{
            'endpoint': '.../api/service',
            'method': 'POST',
            'body': '{"customer": str, "details": str, "amount": float}',
            'description': 'Post the service transaction information'
        }
    ]
    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def service(request):
    if Customer.objects.filter(card_number=request.data.get('customer')).exists():
        customer = Customer.objects.get(card_number=request.data.get('customer'))
        request.data['customer'] = customer.pk
        
        print(f'Data: {request.data}')

        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('[SUCCESS]')
        else:
            return Response('[FAIL]')
    else:
        return Response('[Cardnumber not exist]', status=status.HTTP_404_NOT_FOUND)