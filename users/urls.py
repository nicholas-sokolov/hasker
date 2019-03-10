from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('<str:slug>/', views.ProfileView.as_view(), name='profile'),
]
