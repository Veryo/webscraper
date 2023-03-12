from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.main, name = 'main'),
    path('add_product',views.add_product, name = 'add_product'),
    path('product_list',views.product_list, name = 'product_list'),
    path('product_list/<int:pk>/', views.product_detail, name = 'product_details'),
    path('product/<int:pk>/json/download/', views.download_json, name='download_json'),
    path('product/<int:pk>/xml/download/', views.download_xml, name='download_xml'),
    path('product/<int:pk>/csv/download/', views.download_csv, name='download_csv'),
    path('product/<int:pk>/charts/', views.charts, name='charts'),
    path('about',views.about, name = 'about'),
]
