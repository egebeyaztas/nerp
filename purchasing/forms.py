from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOffer, PurchaseOfferLine

class PurchaseOfferForm(forms.ModelForm):
    class Meta:
        model = PurchaseOffer
        fields = '__all__'

PurchaseLineFormSet = inlineformset_factory(
    parent_model=PurchaseOffer,
    model=PurchaseOfferLine,
    form=PurchaseOfferForm,
    extra=1,
    can_delete=False,
)