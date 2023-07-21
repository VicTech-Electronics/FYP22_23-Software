from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('check/', views.check),
]