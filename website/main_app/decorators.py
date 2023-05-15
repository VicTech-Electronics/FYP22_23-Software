from django.http import HttpResponse
from django.shortcuts import redirect

# Decorators
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'admin':
                    return redirect('admin')
                elif group == 'hospital':
                    return redirect('hospital')
                elif group == 'custormer':
                    return redirect('custormer')
            else:
                return HttpResponse('Sorry, You are not authorized yet, Please conctact us')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def hospital_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return redirect('admin')
            elif group == 'custormer':
                return redirect('custormer')
            elif group == 'hospital':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Sorry, You are not authorized to view this page')
    return wrapper_func


def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return redirect('admin')
            elif group == 'hospital':
                return redirect('hospital')
            elif group == 'custormer':
                return view_func(request, *args, **kwargs)        
        else:
            return HttpResponse('Sorry, You are not authorized to view this page')
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'hospital':
                return redirect('hospital')
            elif group == 'custormer':
                return redirect('custormer')
            elif group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Sorry, You are not authorized to view this page')
    return wrapper_func

