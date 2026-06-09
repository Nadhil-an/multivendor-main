from django import forms
from . models import User,UserProfile
from . validators import form_validation_error


class UserForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("password doesn't match")


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'typing,,,','required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[form_validation_error])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[form_validation_error])

   # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
   # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']

    widgets = {
            'address': forms.TextInput(attrs={'id': 'id_address'}),
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
            'city': forms.HiddenInput(attrs={'id':'id_city'}),
            'state': forms.HiddenInput(attrs={'id':'id_state'}),
            'country': forms.HiddenInput(attrs={'id':"id_country"}),
            'pin_code' : forms.HiddenInput(attrs={'id':"id_pincode"})
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']
    