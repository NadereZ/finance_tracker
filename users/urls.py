from django.urls import path
from . import views


# app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
     path('logout/', views.user_logout, name='logout'),
]
