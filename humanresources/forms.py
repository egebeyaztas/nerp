from django import forms
from .models import *

class PossibleEmployeeForm(forms.ModelForm):
    class Meta:
        model = PossibleEmployee
        fields = '__all__'