from django.urls import path
from merah.views import show_mypay

app_name = 'mypay'

urlpatterns = [
    path('dashboard', show_mypay, name='dashboard'),
]