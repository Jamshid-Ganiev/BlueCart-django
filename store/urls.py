from django.urls import path
from .views import store, product_detail, search, submit_review

app_name = "store"
urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
] 
