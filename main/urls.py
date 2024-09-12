from django.urls import path
from . import views
from main.views import register, index, profile, change_pass, add_propiedad


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/change-pass/', change_pass, name='change_pass'),
    path('propiedad/add-propiedad/', add_propiedad, name='add_propiedad'),
]
