from django.urls import path
from .views import place_order, payments

app_name = "orders"

urlpatterns = [
    path('place_order/', place_order, name="place_order"),
    path('payments/', payments, name='payments'),
    
] 
