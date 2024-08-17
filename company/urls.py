from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.base_view, name='index'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('register/', views.register, name='register'),
    path('query/', views.CompanyQueryView.as_view(), name='query'),
    path('upload/', views.upload_view, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
]