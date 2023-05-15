from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('create/', views.addCase),
]