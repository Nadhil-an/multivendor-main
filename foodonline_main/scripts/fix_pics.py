import os
import django
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodonline_main.settings')
django.setup()

from accounts.models import UserProfile

def create_dummy_image(text, size=(400, 300), color=(73, 109, 137)):
    img = Image.new('RGB', size, color)
    d = ImageDraw.Draw(img)
    d.text((size[0]/4, size[1]/2), text, fill=(255, 255, 0))
    temp_file = BytesIO()
    img.save(temp_file, format='PNG')
    temp_file.seek(0)
    return ContentFile(temp_file.read(), name=f"{text.replace(' ', '_')}.png")

count = 0
for p in UserProfile.objects.all():
    changed = False
    if not p.profile_picture:
        p.profile_picture = create_dummy_image("Profile", (200, 200), (50, 150, 50))
        changed = True
    if not p.cover_photo:
        p.cover_photo = create_dummy_image("Cover", (800, 300), (150, 50, 50))
        changed = True
    
    if changed:
        p.save()
        count += 1

print(f"Fixed missing pictures for {count} profiles.")
