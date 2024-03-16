import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# Create your models here.


class User(AbstractUser):
    full_name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=6,null=True, blank=True,default="User",choices=(("User",'User'),("Staff","Staff")))

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Category(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='CategoryImages/')

    def __str__(self):
        return self.title
    

        
class Product(models.Model):

    prod_category = models.ForeignKey(Category,on_delete=models.CASCADE)

    #Product Basic Info

    prod_id = models.BigIntegerField(unique=True,default=0,null=True,blank=True)
    prod_title = models.CharField(max_length=100,null=True,blank=True)
    prod_description = models.CharField(max_length=100,null=True,blank=True)
    prod_image = models.ImageField(null=True,blank=True,upload_to='ProductImages/')
    prod_price = models.IntegerField(null=True,blank=True)

    #Product Specifications
    prod_brand = models.CharField(max_length=100,null=True,blank=True)
    prod_color = models.CharField(max_length=100,null=True,blank=True)
    prod_weight = models.IntegerField(null=True,blank=True,default=0)
    prod_material = models.CharField(max_length=100,null=True,blank=True)
    prod_dimentions = models.CharField(max_length=100,null=True,blank=True)

    #Stock Information
    prod_stock = models.IntegerField(null=True,blank=True,default=0) 

    #Seller Information
    seller_name = models.CharField(max_length=100,null=True,blank=True)
    seller_address = models.CharField(max_length=100,null=True,blank=True)
    seller_email = models.EmailField(null=True,blank=True)
    
    def save(self, *args, **kwargs):
            if not self.prod_id:
                self.prod_id = self.generate_unique_id()
            super(Product, self).save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            unique_id = random.randint(10**12, 10**13 - 1)
            if not Product.objects.filter(prod_id=unique_id).exists():
                return unique_id
            
    def __str__(self):
        return self.prod_title
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='WishlistItem')

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Feedback(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    feedback = models.CharField(max_length=100,null=True, blank=True)