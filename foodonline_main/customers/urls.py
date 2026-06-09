from django.urls import path,include
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.customerDashboard, name='customerDashboard'),
    path('profile/',views.cprofile,name='cprofile'),
    path('my_order/',views.my_order,name='my_order'),
    path('order_details/<int:order_number>/', views.order_details, name='order_details'),
    path('order_status/', views.order_status, name='order_status'),
    path('check_order_status/<str:order_number>/', views.check_order_status, name='check_order_status'),
    


]