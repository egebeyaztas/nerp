from django import forms
from .models import *
class MarketingForm(forms.ModelForm):
    class Meta:
        model = Marketing
        fields = '__all__'

class PotentialClientForm(forms.ModelForm):
    class Meta:
        model = PotentialClient
        fields = '__all__'

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = '__all__'