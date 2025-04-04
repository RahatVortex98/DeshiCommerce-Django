from django.contrib import admin
from .models import Product,Variation,ReviewRating

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display =('name','price','stock','is_available','category')
    prepopulated_fields ={'slug':('name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display =('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)

admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)


admin.site.register(ReviewRating)
