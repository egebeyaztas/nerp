from django import forms
from .models import Logistic

class LogisticForm(forms.ModelForm):
    class Meta:
        model = Logistic
        fields = '__all__'
