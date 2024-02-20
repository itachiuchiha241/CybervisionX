from django.contrib import admin
from skyline_app.models import product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active']

#admin.site.register(product)
admin.site.register(product,ProductAdmin)