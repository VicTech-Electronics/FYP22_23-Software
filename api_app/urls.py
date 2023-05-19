from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('add/', views.addInfo),
    path('update/', views.updateInfo),
    path('delete/<str:device_num>', views.deleteInfo),
]