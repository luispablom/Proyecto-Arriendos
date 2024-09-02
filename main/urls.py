from django.urls import path
from . import views
from main.views import register, index, profile


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
]
