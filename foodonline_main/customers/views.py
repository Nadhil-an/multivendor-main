from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order,OrderedFood
# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        userprofile_form = UserProfileForm(request.POST,request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST,instance=request.user)
        if userprofile_form.is_valid() and user_form.is_valid():
            userprofile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated')
            return redirect('cprofile')
        else:
            pass # Validation errors are handled in the template
    else:       
        userprofile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context ={
        'user_form':user_form,
        'userprofile_form':userprofile_form,
        'profile':profile,
        
    }

    return render(request,'customer/cprofile.html',context)

def my_order(request):
    recent_orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'recent_orders':recent_orders,
    }
    return render(request,'customer/myorder.html',context)

def order_details(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        context = {
            'order':order,
            'ordered_food':ordered_food,
        }
    except:
        return redirect('customer')
    return render(request,'customer/orderdetails.html',context)

def order_status(request):
    """
    Displays the real-time order tracking dashboard for the latest active order.
    """
    # Fetch the latest active order (is_ordered and not yet Completed/Delivered/Cancelled)
    active_order = Order.objects.filter(
        user=request.user, 
        is_ordered=True
    ).exclude(status__in=['Completed', 'Delivered', 'Cancelled']).order_by('-created_at').first()
    
    context = {
        'order': active_order,
    }
    return render(request, 'customer/order_status.html', context)

from django.http import JsonResponse
def check_order_status(request, order_number):
    """
    JSON endpoint for AJAX polling to check the current status of an order.
    """
    try:
        order = Order.objects.get(order_number=order_number)
        response = {
            'status': order.status,
            'is_ordered': order.is_ordered,
        }
        return JsonResponse(response)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
