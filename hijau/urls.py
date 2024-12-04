from django.urls import path
from . import views

app_name = 'hijau'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('subcategory/<str:category_id>/<str:subcategory_nama>/', views.subcategory_detail, name='subcategory_detail_user'),
    path('join-subcategory/<str:subcategory_id>/<str:pekerja_id>/', views.join_subcategory, name='join_subcategory'),
    path('worker/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    path('create-pemesanan/', views.create_pemesanan, name='create_pemesanan'),
    path('view-pemesanan/', views.view_pemesanan, name='view_pemesanan'),
]
