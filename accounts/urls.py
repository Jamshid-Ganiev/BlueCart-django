from .views import register, login, logout, activate, dashboard, forgotPassword, change_password
from .views import resetpassword_validate, resetPassword, my_orders, edit_profile, order_detail
from django.urls import path

app_name='accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('resetPassword/', resetPassword, name='resetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('my_orders/', my_orders, name='my_orders'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
] 
