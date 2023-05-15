from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def doctor_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'doctor':  
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        else:
            return HttpResponse('You are not allowed to view this page')
    return wrapper_function

def nurse_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'nurse':  
                return view_func(request, *args, **kwargs)
            else:
                return redirect('report')
        else:
            return HttpResponse('You are not allowed to view this page')
    return wrapper_function
    