from django.db import models
from general.models import Client, Product

class Logistic(models.Model):
    status_choices = (
        ('Yüklendi','Yüklendi'),
        ('Yolda','Yolda'),
        ('Teslim edildi','Teslim edildi'),
        ('Termin Bekliyor','Termin Bekliyor'),
    )

    status = models.CharField(max_length=70, blank=False, null=False, choices=status_choices, default=status_choices[0][0])
    client = models.ForeignKey(Client, null=False, blank=False, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, related_name="cargos")
    active = models.BooleanField(default=True)
    logistic_firm_name = models.CharField(max_length=200, blank=True, null=True)
    logistic_firm_phone = models.CharField(max_length=50, blank=True, null=True)
    logistic_firm_email = models.EmailField(max_length=200, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sending_date = models.DateTimeField(auto_now=False, null=True, blank=True, auto_now_add=False)
    cost = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'to: ' + self.client.name + ' at: ' + str(self.created_at)

