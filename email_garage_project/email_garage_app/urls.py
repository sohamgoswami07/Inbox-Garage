from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('brand/', views.brand, name='brand'),
    path('templates/', views.templates, name='templates'),
    path('email/<id>/', views.email_detail, name='email_detail'),
    path('brand/<id>/', views.brand_detail, name='brand_detail'),
]
