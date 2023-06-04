from django.shortcuts import render, redirect
from .models import BreakerState
from api_app.serializers import BreakerStateSerializer

def home_page(request):
    if request.method == 'POST':
        value = request.POST.get('submited_value')
        old_state = BreakerState.objects.get(id=1)
        new_state = {
            'state': value,
        }

        serializer = BreakerStateSerializer(old_state, data=new_state)
        if serializer.is_valid():
            serializer.save()
            print('DOne')
    else:
        new_state = {'state': 'OFF'}

    return render(request, 'home.html', {'data': new_state})
