from django.db import models
from manufacturing.models import JobOrder
from django.contrib.auth.models import User
from general.models import Product

class Quality(models.Model):
    job_order = models.OneToOneField(JobOrder, on_delete=models.CASCADE, blank=True, null=True)
    executive = models.ForeignKey(User, blank=False, null=True, related_name='qualities', limit_choices_to={'groups__name':'executive'}, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True, max_length=2000)
    products = models.ManyToManyField(Product, related_name='qc_orders', blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    qc_id = models.CharField(max_length=100, null=True, blank=True)
    workers = models.ManyToManyField(User, blank=True, null=True, related_name='quality_tasks', limit_choices_to={'groups__name':'worker'})
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return 'Kalite Kontrol Emri - ' + str(self.id) + ' - ' + str(self.created_at)

    def approve(self, product_id):
        if product_id in self.job_order.products.values_list('id', flat=True):
            product = self.job_order.products.get(product_id=product_id)
            product.approved = True
            product.save()
        else:
            return 'Wrong product ID'

    def not_approved(self, product_id):
        if product_id in self.job_order.products.values_list('id', flat=True):
            product = self.job_order.products.get(product_id=product_id)
            product.approved = False
            product.save()
        else:
            return 'Wrong product ID'
