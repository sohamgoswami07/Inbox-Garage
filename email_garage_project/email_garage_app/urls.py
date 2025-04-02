from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('brand/', views.brand, name='brand'),
    path('templates/', views.templates, name='templates'),
    path('blogs/', views.blogs, name='blogs'),
    path('email/<id>/', views.email_detail, name='email_detail'),
    path('blog/<id>/', views.blog_detail, name='blog_detail'),
    path('brand/<id>/', views.brand_detail, name='brand_detail'),
    # path('login/', views.user_login, name='login'),
]
