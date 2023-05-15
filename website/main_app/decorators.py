from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

def unauthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.all().exists():
            group = request.user.groups.all()[0].name
            
            if group == 'nurse':
                return redirect('./')
            elif group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Sorry, You are not authenicated')
            return redirect('./')
            
    return wrapper_func