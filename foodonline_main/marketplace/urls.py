from django.urls import path
from . import views

urlpatterns = [
    # Cart Functions FIRST
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete/<int:food_id>/', views.delete_item, name='delete_item'),

    # Marketplace
    path('', views.marketplace, name='marketplace'),

    # Vendor Routes
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),
    path('<slug:vendor_slug>/<slug:category_slug>/', views.vendor_details, name='vendor_details_by_category'),
]
