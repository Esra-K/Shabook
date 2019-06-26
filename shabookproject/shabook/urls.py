from . import views
from django.urls import path

urlpatterns = [
    path('temp/', views.home, name = 'shabook-home'),
    path('', views.landing, name = 'shabook-landing'),
]