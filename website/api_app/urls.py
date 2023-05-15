from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation, name='documeentation'),
    path('request/', views.req_endpoint, name='req_endpoint'),
    path('response/', views.resp_endpoint, name='resp_endpoint')
]