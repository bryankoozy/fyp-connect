# dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('student/', views.student_home, name='student_home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
]