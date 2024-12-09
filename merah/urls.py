from django.urls import path
from merah.views import show_mypay, transaksi_mypay, pekerja_jasa, status_pekerjaan

app_name = 'merah'

urlpatterns = [
    path('dashboard', show_mypay, name='dashboard'),
    path('transaksi-mypay', transaksi_mypay, name='transaksi_mypay'),
    path('pekerja-jasa', pekerja_jasa, name='pekerja_jasa'),
    path('status-pekerjaan/', status_pekerjaan, name='status_pekerjaan'),
]