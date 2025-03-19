from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('demo-login/', views.demo_login, name="demo_login"),
    path('demo-logout/', views.demo_logout, name="demo_logout"),
]   