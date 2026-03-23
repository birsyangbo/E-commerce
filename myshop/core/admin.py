from django.contrib import admin
from .models import OfferProduct, Category, SubCategory, Product, ProductImage

# Register your models here.
admin.site.register(OfferProduct)
admin.site.register(Category)
admin.site.register(SubCategory)

class ProductAdminImage(admin.TabularInline):
    model = ProductImage
    extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'price', 'discount', 'image')
    inlines = [ProductAdminImage]