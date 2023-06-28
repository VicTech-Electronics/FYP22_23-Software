from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signin, name='login'), 
    path('logout/', views.signout, name='logout'), 
    path('registration/', views.register_user, name='register'),

    path('payment/', views.payment, name='payment'),
    path('notification/', views.notification, name='notification'),
    path('payment_history/', views.payment_history, name='payment_history'),
]