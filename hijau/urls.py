from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('subcategory/<int:category_id>/<str:subcategory_name>/', views.subcategory_detail_user, name='subcategory_detail_user'),
    path('worker/subcategory/<int:category_id>/<str:subcategory_name>/', views.subcategory_detail_worker, name='subcategory_detail_worker'),
    path('worker/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    path('create-pemesanan/', views.create_pemesanan, name='create_pemesanan'),
    path('view-pemesanan/', views.view_pemesanan, name='view_pemesanan'),
]
