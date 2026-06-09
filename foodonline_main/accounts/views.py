from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from . forms import UserForm
from . models import User
from vendor.forms import VendorForm
from .models import UserProfile
from . utilis import detectUser,send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor 
from django.template.defaultfilters import slugify
from django.db.models import Sum
from orders.models import Order
import datetime
from menu.models import Category
# Create your views here.


#Restrict the vendor from acessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
#Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
# -----------------------------
# Customer Registration
# -----------------------------

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'Already registered')
        return redirect('myaccount')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER       
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been registered successfully! You can now log in.')
            return redirect('loginUser')
           
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/userRegister.html', context)

# -----------------------------
# Vendor Registration
# -----------------------------

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered')
        return redirect('myaccount')

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            # Create user
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.role = User.RESTAURANT
            user.save()
            # Create vendor
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            messages.success(request, 'Your account has been registered successfully! Please wait for approval.')
            return redirect('loginUser')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {'form': form, 'v_form': v_form}
    return render(request, 'accounts/registerVendor.html', context)


# -----------------------------
# User Login
# -----------------------------

def loginUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are  already logged in')
        return redirect('myaccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            # messages.success(request,'successfully login')
            return redirect('myaccount')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('loginUser')

    return render(request,'accounts/login.html')

# -----------------------------
# User Logout
# -----------------------------

def logout(request):
    auth.logout(request)
    messages.info(request,'you are logged out')
    return redirect('loginUser')

# -----------------------------
# Dashboard Redirection
# -----------------------------  
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vendorhome(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).prefetch_related("fooditems")


    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request,'vendor_home.html',context)




@login_required(login_url='login/')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True)
    recent_orders = Order.objects.filter(user=request.user,is_ordered=True)[:5]
    orders_count = orders.count()
    # Calculate total spent
    total_spent = orders.aggregate(Sum('total'))['total__sum']
    if total_spent is None:
        total_spent = 0
    
    context = {
        'orders':orders,
        'orders_count':orders_count,
        'recent_orders':recent_orders,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/customerdashboard.html',context)


# -----------------------------
# Dashboard Views
# -----------------------------
@login_required(login_url='loginUser')
def myaccount(request):
    if request.user.is_authenticated:
        redirecturl = detectUser(request.user)
        return redirect(redirecturl)
    else:
        return redirect('loginUser')
    

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        # messages.success(request,'Account has been activated')
        return redirect('myaccount')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('myaccount')
    

# -----------------------------
# forgot password
# -----------------------------
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)


            # send reset email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, email_template, mail_subject)
            messages.success(request, 'Reset Email has been sent')
            
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')

    return render(request, 'accounts/forgotpassword.html')

# -----------------------------
# Reset Password
# -----------------------------
def reset_password_validate(request,uidb64, token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please reset the password')
        return redirect ('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('Myaccount')

def reset_password(request):
    uid = request.session.get('uid')
    if not uid:
        messages.error(request, 'Unauthorized access!')
        return redirect('myaccount')


    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            # messages.success(request,'Password reset successfully')
            return redirect('loginUser')

        
        else:
            messages.error(request,'Password does not match')
            return redirect('reset_password')


    return render(request,'accounts/resetpassword.html')

