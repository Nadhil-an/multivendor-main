from django.contrib import admin
from .models import Payment, Order, OrderedFood


class OrderFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order','payment','user','fooditem','quantity','price','amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','phone','email','total','payment_method','order_placed_to','status','is_ordered']
    inlines = [OrderFoodInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'payment_method', 'amount', 'status']


@admin.register(OrderedFood)
class OrderedFoodAdmin(admin.ModelAdmin):
    list_display = ['order', 'fooditem', 'quantity', 'price', 'amount']


admin.site.register(Order, OrderAdmin)
