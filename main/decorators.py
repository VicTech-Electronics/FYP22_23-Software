from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Customer



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'customer':
                user_id = request.user.pk
                customer = Customer.objects.get(user = user_id)
                return redirect('home', customer.pk)
            elif group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Sorry you are not authenticated, Please contact us')
    return wrapper_func


def unauthorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func