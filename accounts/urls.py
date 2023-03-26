from .views import register, login, logout, activate, dashboard
from django.urls import path

app_name='accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),

] 
