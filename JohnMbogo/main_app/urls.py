from unicodedata import name
from django.urls import path
from . import views
from . import functions


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('report/', views.report, name='report'),
    path('doctor/<str:report>', views.doctor, name='doctor'),

    # Function urls
    path('generate_code_PDF/<str:code>', functions.generate_code_PDF, name='generate_code_PDF'),
    path('generate_treatment_advice_PDF/<str:code>/<str:advice>', functions.generate_treatment_advice_PDF, name='generate_treatment_advice_PDF')
]