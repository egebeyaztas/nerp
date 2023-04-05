from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from .models import *

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(BalanceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['net_income'].label = 'Net Gelir'
        self.fields['brute_income'].label = 'Ciro'
        self.fields['total_balance'].label = 'Toplam Gelir'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['name'].label = 'Gelir Adı'
        self.fields['amount'].label = 'Tutar'
        self.fields['description'].label = 'Açıklama'
        self.fields['income_date'].label = 'Geliş Tarihi'
        self.fields['order'].label = 'Sipariş'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ['line_name', 'line_quantity','line_unit_price','line_total_price']

InvoiceLineFormSet = inlineformset_factory(
    Invoice,
    InvoiceLine,
    InvoiceForm,
    can_delete = False,
    extra=1,
)

