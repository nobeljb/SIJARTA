from django.urls import path
from biru.views import *

app_name = 'biru'

urlpatterns = [
    path('diskon/', diskon, name='diskon'),
    path('testimoni-form/', testimoni_form, name='testimoni_form'),
    path('pembelian-voucher/', pembelian_voucher, name='pembelian_voucher'),
    path('testimoni-cards/', testimoni_cards, name='testimoni_cards')
]
