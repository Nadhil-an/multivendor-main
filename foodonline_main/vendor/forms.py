from django import forms
from . models import Vendor,OpeningHour
from accounts.validators import form_validation_error



class VendorForm(forms.ModelForm):
    vendor_licence = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[form_validation_error])
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_licence']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day','from_hour','to_hour','is_closed']

     