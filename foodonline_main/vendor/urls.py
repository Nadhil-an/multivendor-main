from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.vendorhome,name='vendorhome'),
    path('Dashboard/',views.vendorDashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('menu-builder/',views.menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/',views.fooditems_by_category,name='fooditems_by_category'),

    # Categoty CRUD OPERATIONS
    path('menu-builder/category/add/',views.add_category,name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category,name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/',views.delete_category,name='delete_category'),

    #FoodItems CRUD OPERATIONS
    path('menu-builder/food/add-food/',views.addfood,name='addfood'),
    path('menu-builder/food/edit/<int:pk>/',views.edit_food,name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/',views.delete_food,name='delete_food'),

    #opening Hour CRUD OPERATIONS
    path('opening-hours/',views.opening_hours,name='opening_hours'),
    path('add-hour/',views.add_hour,name='add_hour'),
    path('add-hour/remove/<int:pk>/',views.removing_opening_hour,name='removing_opening_hour'),

    path('vendor_order_details/<int:order_number>/',views.vendor_order_details,name='vendor_order_details'),
    path('order/update-status/<str:order_number>/', views.update_order_status, name='update_order_status'),
    path('orders/',views.vendor_orders,name='vendor_orders'),



]
