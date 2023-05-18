from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TransactionSerializer
from rest_framework import status
from main.models import Customer


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
            'endpoint': '.../api/payment',
            'methode': 'POST',
            'body': '{"card_number": str, "amount": float, "details": str}',
            'description': 'Adding a new payment infomation details'
        }
    ]
    return Response(info, status=status.HTTP_200_OK)

@api_view(['POST'])
def payment(request):
    customer = Customer.objects.get(card_no = request.data.get('card_number'))
    payment_data = {
        'customer': customer.pk,
        'amount': request.data.get('amount'),
        'details': request.data.get('details'),
    }

    serializer = TransactionSerializer(data = payment_data)
    if serializer.is_valid():
        remained_balance = customer.amount - request.data.get('amount')

        if remained_balance >= 0:
            customer.amount = remained_balance
            customer.save()
            serializer.save()
            return Response('SUCCESS')
        else:
            return Response('Insufficient balance', status=status.HTTP_402_PAYMENT_REQUIRED)
    else:
        return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)
    