from django.shortcuts import render,get_object_or_404,redirect
from . models import Vendor,OpeningHour
from django.http import HttpResponse,JsonResponse
from .forms import VendorForm,OpeningHourForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from django.conf import settings
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify  
from django.views.decorators.cache import never_cache
from orders.models import Order,OrderedFood
import datetime



def vendorDashboard(request):
    """
    Displays the vendor dashboard with current and past orders, revenue stats, and insights.
    """
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendor__in=[vendor.id], is_ordered=True).order_by('-created_at')
    
    # Filter orders
    current_orders = orders.filter(status__in=['New', 'Accepted'])
    history_orders = orders.filter(status__in=['Completed', 'Delivered', 'Cancelled'])
    
    recent_orders = orders[:3]

    total_revenue = 0
    for i in orders.filter(status__in=['Completed', 'Delivered']):
        total_revenue += i.get_total_by_vendor()['grand_total']

    # monthly revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(
        vendor__in=[vendor.id], 
        created_at__month=current_month,
        status__in=['Completed', 'Delivered']
    )
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    context = {
        'vendor': vendor,
        'current_orders': current_orders,
        'history_orders': history_orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'vendor/vendorDashboard.html', context)

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def update_order_status(request, order_number):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            order = Order.objects.get(order_number=order_number)
            order.status = status
            order.save()
            messages.success(request, f'Order #{order_number} status updated to {status}')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
        
    return redirect('vendor')

##################################
#
# Create Vendor Profile
#
###################################

# Create your views here.
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vprofile(request):
    
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor_get = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor_get)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings Updated.')
            return redirect('vprofile')
        else:
            pass # Validation errors are handled in the template
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor_get)

    
    context = {
        'profile':profile,
        'vendor_get':vendor_get,
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        
    }
    
    return render(request,'vendor/vprofile.html',context)

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


##################################
#
# Menu Builder
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    category = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'category':category
    }
    return render(request,'vendor/menu_builder.html',context)



##################################
#
# Food_items by category
#
###################################
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'category':category,
        'fooditems':fooditems
    }
    return render(request,'vendor/menu_category.html',context)

##################################
#
# Add Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()

            category.slug = slugify(category_name)+'-'+str(category.id) # ✅ assign vendor
            category.save()
              # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category added Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()

    # ✅ context is always defined
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


##################################
#
# Edit Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST,instance=category)
    if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)  # ✅ assign vendor
            category.save()  # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category updated Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)

    # ✅ context is always defined
    context = {
        'form': form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)

##################################
#
# Delete Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()

    messages.success(request,'Category Successfully delete')
    return redirect('menu_builder') 


##################################
#
# Add Food Item
#
###################################


@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)    
def addfood(request):

    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug= slugify(food_title) 
            food.save() 
            messages.success(request, 'Food Successfully Added')
            return redirect('fooditems_by_category',food.category.id)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form':form
        
    }
    return render(request,'vendor/addfood.html',context)


##################################
#
# Edit food item
#
###################################
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST,request.FILES,instance=food )
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        if form.is_valid():
                food = form.save(commit=False)
                food.vendor = get_vendor(request)  # ✅ assign vendor
                food.save()  # ✅ slug auto-handled in model.save()
                messages.success(request, 'FoodItem updated Successfully')
                return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=food)  
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    # ✅ context is always defined
    context = {
        'form': form,
        'food':food,
    }
    return render(request,'vendor/edit_food.html',context)
##################################
#
# Edit food item
#
###################################
@login_required(login_url='loginUser')
def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()

    messages.success(request,'Food item delete successfully ')
    return redirect('menu_builder') 


##################################
#
# Opening Hours
#
###################################
def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm() 
    context = {
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request,'vendor/opening_hours.html',context)

##################################
#
# add Hours
#
###################################
def add_hour(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                vendor = get_vendor(request)
                day = int(day)
                is_closed = True if is_closed in ['True', 'true', True] else False

                # ✅ Closed case
                if is_closed:
                    has_open_slots = OpeningHour.objects.filter(vendor=vendor, day=day, is_closed=False).exists()
                    if has_open_slots:
                        return JsonResponse({
                            'status': 'failed',
                            'message': 'Cannot mark as closed — this day already has open time slots!'
                        })
                    has_closed_slots = OpeningHour.objects.filter(vendor=vendor, day=day, is_closed=True).exists()
                    if has_closed_slots:
                        return JsonResponse({
                            'status': 'failed',
                            'message': 'This day is already marked as closed!'
                        })

                    # ✅ Create a closed hour record
                    hour = OpeningHour.objects.create(
                        vendor=vendor,
                        day=day,
                        from_hour='',
                        to_hour='',
                        is_closed=True
                    )

                # ✅ Open case
                else:
                    is_this_day_closed = OpeningHour.objects.filter(vendor=vendor, day=day, is_closed=True).exists()
                    if is_this_day_closed:
                        return JsonResponse({
                            'status': 'failed',
                            'message': 'Cannot add a time slot — this day is marked as closed!'
                        })

                    exists = OpeningHour.objects.filter(
                        vendor=vendor,
                        day=day,
                        from_hour=from_hour,
                        to_hour=to_hour,
                        is_closed=False
                    ).exists()

                    if exists:
                        day_name = dict(OpeningHour._meta.get_field('day').choices).get(day, 'Unknown Day')
                        return JsonResponse({
                            'status': 'failed',
                            'message': f'{day_name} {from_hour} - {to_hour} already exists!'
                        })

                    # ✅ Create a new open slot
                    hour = OpeningHour.objects.create(
                        vendor=vendor,
                        day=day,
                        from_hour=from_hour,
                        to_hour=to_hour,
                        is_closed=False
                    )

                # ✅ Common response (works for both open & closed)
                response = {
                    'status': 'success',
                    'id': hour.id,
                    'day': hour.get_day_display(),
                    'from_hour': hour.from_hour,
                    'to_hour': hour.to_hour,
                    'is_closed': hour.is_closed,
                }
                return JsonResponse(response)

            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': str(e)})

        return HttpResponse('Invalid request')
    return HttpResponse('Unauthorized', status=401)



def removing_opening_hour(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({
                'status':'success','id':pk 
            })
        else:
            return HttpResponse('Invalid request')


    else:
        return HttpResponse('Unauthorized', status=401)


def vendor_order_details(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order,fooditem__vendor=get_vendor(request))
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal': order.get_total_by_vendor()['sub_total'],
            'tax_data':order.get_total_by_vendor()['tax_dict'],
            'grand_total':order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')


    return  render(request,'vendor/vendor_order_details.html',context)

def vendor_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(
        vendor__in=[vendor.id], 
        is_ordered=True,
        status__in=['Completed', 'Delivered', 'Cancelled']
    ).order_by('-created_at')
    context = {
        'order': orders,
    }
    return render(request, 'vendor/vendor_orders.html', context)
