from django import forms
from .models import Category,FoodItem
from accounts.validators import form_validation_error

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']


class FoodItemForm(forms.ModelForm):
     food_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Food Name'}))
     price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Price of Food'}))
     image = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[form_validation_error])
     class Meta:
         model = FoodItem
         fields = ['category','food_title','description','price','image','is_available']

