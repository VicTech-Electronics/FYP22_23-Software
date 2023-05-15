from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation),
    path('create/', views.create),
    path('confirm/', views.confirm),
    path('cancel/<str:vehicle_number>', views.cancel),
]