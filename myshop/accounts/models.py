from django.db import models
from django.contrib.auth.models import User ,AbstractUser
# Create your models here.
 
class CustomUser(AbstractUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    email=models.EmailField(unique=True)
    address=models.TextField(null=True,blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',null=True,blank=True)

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user=models.OneToOneField(CustomUser,related_name='profile', on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pics',null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username