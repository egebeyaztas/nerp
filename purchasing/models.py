from django.db import models
from general.models import Stock, StockGroup, Supplier

class PurchaseOffer(models.Model):

    status_choices = (
        ('Bekliyor','Bekliyor'),
        ('Onaylandı','Onaylandı'),
        ('Reddedildi','Reddedildi'),
    )

    supplier = models.ForeignKey(Supplier, related_name="offers", blank=False, null=False, on_delete=models.CASCADE)
    currency_type = models.CharField(max_length=10, blank=False, null=False, default="TRY")
    approve_status = models.CharField(max_length=100, blank=False, null=False, choices=status_choices, default=status_choices[0][0])
    offer_id = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.supplier.name + '- Satın Alma Teklifi - ' + str(self.date_created)

class PurchaseOfferLine(models.Model):
    stock = models.ForeignKey(Stock, related_name='purchase_offer_lines', blank=False, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=True)
    offer = models.ForeignKey(PurchaseOffer, related_name='lines', blank=True, null=True, on_delete=models.CASCADE)
    unit_price = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.stock.name
