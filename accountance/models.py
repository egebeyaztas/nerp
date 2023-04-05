from django.db import models
from general.models import Order
from purchasing.models import PurchaseOffer


class Invoice(models.Model):
    comments = models.TextField(max_length=3000, default='', blank=True, null=True)
    invoice_id = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    waybill_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    waybill_no = models.CharField(max_length=200, blank=True, null=True)
    tax_no = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField('Customer Name', max_length=120, default='', blank=True, null=True)
    customer_adress = models.TextField(max_length=1200, blank=True, null=True)
    phone_number = models.CharField(max_length=120, default='', blank=True, null=True)
    total = models.IntegerField(default='0', blank=True, null=True)
    balance = models.IntegerField(default='0', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)
    order = models.OneToOneField(Order, blank=True, null=True, related_name='invoice', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    invoice_type_choice = (
			('Fiş', 'Fiş'),
			('Proforma Fatura', 'Proforma Fatura'),
			('Fatura', 'Fatura'),
		)
    invoice_type = models.CharField(max_length=50, default='', blank=True, null=True, choices=invoice_type_choice)

    def __str__(self):
	    return str(self.id)

class InvoiceLine(models.Model):
    line_name = models.CharField('Line', max_length=120, default='', blank=True, null=True)
    line_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, blank=False, null=False, on_delete=models.CASCADE, related_name='lines')

    def __str__(self):
        return self.line_name or ''

class Balance(models.Model):
    total_balance = models.IntegerField(default='0', blank=False, null=False)
    brute_income = models.IntegerField(default='0', blank=False, null=False)
    net_income = models.IntegerField(default='0', blank=False, null=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)

class Expense(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=1200, blank=True, null=True)
    expense_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    purchase = models.OneToOneField(PurchaseOffer, related_name='purchase_offer', blank=True, null=True, on_delete=models.SET_NULL)
    expense_type_choices = (
        ('Sigorta','Sigorta'),
        ('Vergi', 'Vergi'),
        ('Satın Alım', 'Satın Alım'),
        ('Diğer', 'Diğer'),
    )
    expense_type = models.CharField(max_length=70, blank=False, null=False, choices=expense_type_choices)

    def __str__(self):
        if self.expense_date:
            return self.name + " - " + str(self.expense_date)
        return self.name


class Income(models.Model):
    paying_choices = (
        ('Nakit','Nakit'),
        ('EFT/Havale','EFT/Havale'),
        ('Diğer','Diğer'),
    )
    name = models.CharField(max_length=250, blank=False, null=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=1200, blank=True, null=True)
    income_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    payment_type = models.CharField(max_length=100, choices=paying_choices, null=True, blank=True)
    
    def __str__(self):
        if self.income_date:
            return self.name + " - " + str(self.income_date)
        return self.name