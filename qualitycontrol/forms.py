from django import forms
from .models import Quality
from general.models import Product
class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = '__all__'

class ApproveForm(forms.Form):
    field = forms.BooleanField(label=('Onay'), widget=forms.CheckboxInput(attrs={'onchange': 'submit();'}))