from django.urls import path
from . import views

urlpatterns = [
    path('<str:vehicle_id>', views.classify, name='classifier'),
]