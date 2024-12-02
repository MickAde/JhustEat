from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user_type_choice = [
        ('Customer' , 'CUSTOMER'),
        ('Driver' , 'DRIVER'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(choices=user_type_choice, max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to='Profile_Image', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=215, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    
class Category(models.Model):
    name = models.CharField(max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Menu_Categories')
 
    def __str__(self):
        return self.name
    
    
class Menu(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.DO_NOTHING)
    quantity_available = models.PositiveIntegerField(null=True, blank=True)
    price_per_unit = models.FloatField()
    delivery_charge = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='Menu_Categories')
    rating = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    status_list = [
        ('Order Being Prepared', 'Order Being Prepared'),
        ('Delivering To You', 'Delivering To You'),
        ('Order Completed', 'Order Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(Menu, verbose_name="Dishes", on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    total_price = models.FloatField()
    address = models.CharField(max_length=500)
    status = models.CharField(choices=status_list, max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name} at {self.date_added}"


class Promo(models.Model):
    percent_discount = models.IntegerField()
    menu = models.ForeignKey(Menu, verbose_name="Dishes", on_delete=models.DO_NOTHING)
    end_date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        menu_old_price = int(self.menu.price_per_unit)
        percentage = int(self.percent_discount) / 100
        
        menu_new_price = percentage * menu_old_price
        self.menu.price_per_unit = menu_new_price
        self.menu.price_per_unit.save()
                
        return super().save(*args, **kwargs)
    
    
class Notification(models.Model):
    notification_type_list = [
        ('Order', 'Order'),
        ('Offer', 'Offer'),
        ('Update', 'Update'),
    ]
    title = models.CharField(max_length=500)
    sub_title = models.CharField(max_length=500)
    note = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(choices=notification_type_list, max_length=150)
