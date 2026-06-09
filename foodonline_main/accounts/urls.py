from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.myaccount),
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword/',views.reset_password,name='resetpassword'),
    
   
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('vendor/',include('vendor.urls')),
    path('customer/',include('customers.urls')),

]
