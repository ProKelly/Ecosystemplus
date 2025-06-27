from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.calculate_emissions, name='calculate_emissions'),
    path('form-options/', views.get_form_options, name='form_options'),
    path('health/', views.health_check, name='health_check'),
]
