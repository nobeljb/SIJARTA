from django.urls import path
from kuning.views import *

app_name = 'kuning'

urlpatterns = [
    path('show_profile/', show_profile, name='show_profile'),
    path('register/', choose_role, name='choose_role'),
    path('register/register_pekerja/', register_pekerja, name='register_pekerja'),
    path('login', login, name='login'),
    path('register_pengguna', register_pengguna, name='register_pengguna'),
    path('logout', logout, name='logout'),
    path('update_pekerja', update_pekerja, name='update_pekerja'),
    path('update_pengguna', update_pengguna, name='update_pengguna'),
]