from django.db import models
import string, random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Client(models.Model):

    name = models.CharField(max_length=250, blank=False, null=False)
    client_id = models.CharField(max_length=100, blank=False, null=False, default='')
    mail = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    representative_name = models.CharField(max_length=200, blank=True, null=True)
    representative_phone = models.CharField(max_length=50, blank=True, null=True)
    representative_mail = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

def qs_for_products():
    choice_list = []
    names = Client.objects.values_list('name', flat=True)
    for name in names:
        name_tuple = (name,name)
        choice_list.append(name_tuple)
    choice_tuple = tuple(choice_list)
    return choice_tuple
class ProductGroup(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    product_id = models.CharField(max_length=100, blank=False, null=False, default='')
    description = models.TextField(max_length=3000, blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=None, null=True, blank=True)
    job_order = models.ForeignKey('manufacturing.JobOrder', blank=False, null=True, on_delete=models.SET_NULL, related_name='products')
    product_group = models.ForeignKey(ProductGroup, blank=False, null=True, on_delete=models.CASCADE, related_name='products')
    order = models.ForeignKey('Order', blank=False, null=True, on_delete=models.SET_NULL, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product_group.name + ' - ' + self.client.name + ' - ' + self.product_id

    def has_price(self):
        if self.price:
            return True
        return False
    
    def has_clients(self):
        if self.client:
            return True
        return False

class Order(models.Model):
    name = models.CharField(max_length=190, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    order_id = models.CharField(max_length=120, blank=True, null=True)
    order_notes = models.TextField(max_length=1200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.client.name + ' - order no: ' + str(self.id)

    def get_first_product_group(self):
        return self.orderlines.all().first().product_group

    def get_first_product_quantity(self):
        return self.orderlines.all().first().quantity

class OrderLine(models.Model):
    product_group = models.ForeignKey(ProductGroup, related_name='orderlines', on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderlines')

    def __str__(self):
        return self.product_group.name

class StockGroup(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    description = models.TextField(max_length=1200, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    stock_group = models.ForeignKey(StockGroup, related_name="stocks", on_delete=models.CASCADE, blank=False, null=True)
    in_purchase_list = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def add_to_purchase_list(self):
        self.in_purchase_list = True
        self.save()
    
    def remove_from_purchase_list(self):
        self.in_purchase_list = False
        self.save()

class Supplier(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    executive = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    mail = models.EmailField(max_length=200, blank=True, null=True)
    supplier_id = models.CharField(max_length=100, blank=True, null=True)
    sells = models.ManyToManyField(Stock, blank=True, null=True, related_name="suppliers")

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    occupation = models.CharField(max_length=200, blank=False, null=False)
    age = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f'profile created for {instance.username}')
