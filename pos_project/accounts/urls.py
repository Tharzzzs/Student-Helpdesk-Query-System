from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('requests/<int:id>/', views.request_detail, name='request_detail'),

]
