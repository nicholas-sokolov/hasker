from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('<str:slug>/', views.ProfileView.as_view(), name='profile'),
]
