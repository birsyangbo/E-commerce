from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import CustomUser

# Create your models here.
class OfferProduct(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='offer_products/', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    title=models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    desc=CKEditor5Field('text', config_name='extends')
    mark_price=models.DecimalField(max_digits=10, decimal_places=2)
    price=models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    image=models.ImageField(upload_to='products/', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    discount=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active=models.BooleanField(default=True)
    update_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.price = self.mark_price *(1- self.discount/100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='product_images/')




class Review(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE , related_name='reviews')
    rating=models.PositiveSmallIntegerField()
    feedback=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"