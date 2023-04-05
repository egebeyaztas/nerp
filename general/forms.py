from django import forms
from django.forms import modelform_factory, inlineformset_factory, BaseModelFormSet

from .models import *
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'client', 'price']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderlineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = '__all__'


OrderLineFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderLine,
    form=OrderForm,
    extra=0,
    can_delete=False,
)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'