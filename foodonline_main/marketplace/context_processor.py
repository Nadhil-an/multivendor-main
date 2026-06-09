from .models import Cart
from menu.models import FoodItem
from marketplace.models import Tax

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:

            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    cart_count += item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return  dict(cart_count=cart_count)


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict ={}

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            food_item = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (food_item.price * item.quantity)
        

        # Taxes are disabled as per user request
        tax = 0
        tax_dict = {}
        grand_total = subtotal
           
    return dict(subtotal=subtotal,tax=tax,grand_total=grand_total,tax_dict=tax_dict)
