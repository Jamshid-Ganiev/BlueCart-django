from .views import register, login, logout
from django.urls import path

app_name='accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
   

] 
