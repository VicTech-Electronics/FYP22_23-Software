from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('usage/', views.usage),
    path('notification/', views.notification),
]