from django.urls import path
from landing_page.views import show_landing_page

app_name = 'landing_page'

urlpatterns = {
    path('', show_landing_page, name='landing_page',)
}