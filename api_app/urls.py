from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('call/', views.call),
    path('report/', views.report),
    path('message/', views.message),
]