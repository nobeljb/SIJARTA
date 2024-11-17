from django.urls import path
from kuning.views import *

app_name = 'kuning'

urlpatterns = {
    path('show_profile', show_profile, name='show_profile'),
    path('register', choose_role, name='register'),
    path('register_pekerja', register_pekerja, name='register_pekerja'),
}