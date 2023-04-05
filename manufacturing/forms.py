from django.forms import ClearableFileInput
from django import forms
from .models import JobOrder, JobOrderFile, TaskFlow, Task

class JobOrderModelForm(forms.ModelForm):
    class Meta:
        model = JobOrder
        fields = ['executive', 'product_quantity', 'client', 'deadline']
        widgets = {
            'workers': forms.CheckboxSelectMultiple,
        }

class FileModelForm(forms.ModelForm):
    class Meta:
        model = JobOrderFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('finish_time', 'is_finished',)
        widgets = {
            'workers': forms.CheckboxSelectMultiple,
        }