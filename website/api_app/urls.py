from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('examine/', views.examine),
]