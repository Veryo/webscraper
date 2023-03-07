from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.add_product, name = 'add_product'),
    path('product_list',views.product_list, name = 'product_list'),
    path('product_list/<int:pk>/', views.product_detail, name = 'product_list'),
]
