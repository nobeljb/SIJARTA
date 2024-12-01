from django.urls import path
from .views import *

urlpatterns = [
    path('', show_pengguna, name='show_pengguna'),
]