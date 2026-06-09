import os
import django
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodonline_main.settings')
django.setup()

from accounts.models import User, UserProfile
from vendor.models import Vendor
from menu.models import Category, FoodItem

def create_dummy_image(text, size=(400, 300), color=(73, 109, 137)):
    img = Image.new('RGB', size, color)
    d = ImageDraw.Draw(img)
    d.text((size[0]/4, size[1]/2), text, fill=(255, 255, 0))
    temp_file = BytesIO()
    img.save(temp_file, format='PNG')
    temp_file.seek(0)
    return ContentFile(temp_file.read(), name=f"{text.replace(' ', '_')}.png")

print("Creating Test Restaurant 1...")
# Rest 1
u1, created = User.objects.get_or_create(email='rest1@gmail.com', defaults={'first_name':'John', 'last_name':'Doe', 'username':'rest1', 'role':User.RESTAURANT})
if created:
    u1.set_password('password123')
    u1.save()

p1, _ = UserProfile.objects.get_or_create(user=u1)
p1.address = "123 Burger St"
p1.city = "New York"
p1.latitude = 40.7128
p1.longitude = -74.0060
p1.save()

v1, _ = Vendor.objects.get_or_create(
    user=u1,
    defaults={
        'user_profile': p1,
        'vendor_name': "Burger King",
        'vendor_slug': "burger-king",
        'is_approved': True,
        'vendor_licence': create_dummy_image("License", (100,100))
    }
)

c1, _ = Category.objects.get_or_create(vendor=v1, category_name="Burgers", slug="burgers")

FoodItem.objects.get_or_create(
    vendor=v1,
    slug="cheeseburger",
    defaults={
        'category': c1,
        'food_title': "Cheeseburger",
        'description': "Delicious cheese burger",
        'price': 5.99,
        'image': create_dummy_image("Cheeseburger"),
        'is_available': True
    }
)

FoodItem.objects.get_or_create(
    vendor=v1,
    slug="double-whopper",
    defaults={
        'category': c1,
        'food_title': "Double Whopper",
        'description': "Double meat",
        'price': 8.99,
        'image': create_dummy_image("Double Whopper"),
        'is_available': True
    }
)


print("Creating Test Restaurant 2...")
# Rest 2
u2, created = User.objects.get_or_create(email='rest2@gmail.com', defaults={'first_name':'Jane', 'last_name':'Doe', 'username':'rest2', 'role':User.RESTAURANT})
if created:
    u2.set_password('password123')
    u2.save()

p2, _ = UserProfile.objects.get_or_create(user=u2)
p2.address = "456 Pizza Ave"
p2.city = "New York"
p2.latitude = 40.7150
p2.longitude = -74.0100
p2.save()

v2, _ = Vendor.objects.get_or_create(
    user=u2,
    defaults={
        'user_profile': p2,
        'vendor_name': "Pizza Hut",
        'vendor_slug': "pizza-hut",
        'is_approved': True,
        'vendor_licence': create_dummy_image("License", (100,100))
    }
)

c2, _ = Category.objects.get_or_create(vendor=v2, category_name="Pizzas", slug="pizzas")

FoodItem.objects.get_or_create(
    vendor=v2,
    slug="pepperoni-pizza",
    defaults={
        'category': c2,
        'food_title': "Pepperoni Pizza",
        'description': "Classic pepperoni",
        'price': 12.99,
        'image': create_dummy_image("Pepperoni Pizza", color=(200, 50, 50)),
        'is_available': True
    }
)

FoodItem.objects.get_or_create(
    vendor=v2,
    slug="margherita",
    defaults={
        'category': c2,
        'food_title': "Margherita",
        'description': "Cheese and tomato",
        'price': 10.99,
        'image': create_dummy_image("Margherita", color=(50, 200, 50)),
        'is_available': True
    }
)

print("Successfully created 2 test restaurants with dummy images and items!")
