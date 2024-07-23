from django.urls import path
from .views import generate_password,index

urlpatterns = [
    path('', index, name='index'),
    path('generate/', generate_password, name='generate_password'),
]
