from django.shortcuts import render, redirect
from .models import PlateNumber, CardNumber
from django.contrib import messages

# Create your views here.
def mainPage(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        action = request.POST.get('action')
        type = request.POST.get('type')

        if type == 'plate':
            Database = PlateNumber
            object_title = 'Plate number'
        elif type == 'card':
            Database = CardNumber
            object_title = 'Card number'

        if action == 'add':
            if Database.objects.filter(number=number).exists():
                messages.error(request, f'Sorry! {object_title}: {number}, Alread exist to the database.')
            else:
                object = Database.objects.create(number=number)
                object.save()
                messages.success(request, f'{object_title}: {number}, added successful to the database')

        elif action == 'delete':   
            if Database.objects.filter(number=number).exists():
                object = Database.objects.get(number=number)
                object.delete()
                messages.success(request, f'{object_title}: {number}, deleted successful')
            else:
                messages.error(request, f'Sorry! {object_title}: {number}, Not exist in the database')
        
        return redirect('main_page')

    return render(request, 'index.html')