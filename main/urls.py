from django.urls import path
from . import views
from main.views import register, index


urlpatterns = [
    path('', views.index, name='index'),
    path('acounts/register/', register, name='register'),
]
