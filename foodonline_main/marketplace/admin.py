from django.contrib import admin
from . models import Cart,Tax

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','updated_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type','tax_percentage','is_active')
    
    class Meta:
        verbose_name_plural ='taxes'


admin.site.register(Cart,CartAdmin)
admin.site.register(Tax,TaxAdmin)
