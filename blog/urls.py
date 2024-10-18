# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create/', views.create_blog, name='create_blog'),
    path('edit/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]
