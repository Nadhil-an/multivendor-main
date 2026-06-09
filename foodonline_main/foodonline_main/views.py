from django.shortcuts import render,redirect
from vendor.models import Vendor
from accounts.models import User
from .utils import haversine_distance


def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['long']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('long')
        request.session['lat'] = lat
        request.session['long'] = lng
        return lng, lat
    else:
        return None


def home(request):

    # If vendor → redirect to vendor dashboard
    if request.user.is_authenticated and request.user.role == User.RESTAURANT:
        return redirect('vendorhome')

    # If customer → allow them to view home.html (NO redirect needed)
    # So do NOT redirect customers

    location = get_or_set_current_location(request)

    if location is not None:
        lng, lat = location
        lat = float(lat)
        lng = float(lng)
        
        all_vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
        vendors = []
        for v in all_vendors:
            if v.user_profile.latitude and v.user_profile.longitude:
                dist = haversine_distance(lat, lng, v.user_profile.latitude, v.user_profile.longitude)
                if dist <= 1000:
                    v.km = round(dist, 1)
                    vendors.append(v)
        
        vendors.sort(key=lambda x: x.km)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]

    return render(request, 'home.html', {'vendors': vendors})

