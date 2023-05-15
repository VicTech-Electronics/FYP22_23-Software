from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin'),
    path('hospital/', views.hospital_dashboard, name='hospital'),
    path('account/', views.custormer_dashboard, name='custormer'),
    path('hospital_reg/', views.register_hospital, name='hospital_reg'),
    path('user_reg/', views.register_user, name='user_reg'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
    path('location/<int:pk>', views.location, name='location'),
]