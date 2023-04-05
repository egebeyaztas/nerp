from django.db import models

def file_path(instance, filename):
    try:
        return f'human_resources/cv/{str(instance.name)}/{filename}'
    except Exception as e:
        print(e)

class PossibleEmployee(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    surname = models.CharField(max_length=120, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    occupation = models.CharField(max_length=200, blank=False, null=False)
    age = models.IntegerField(blank=True, null=True)
    status_choices = (
        ('Yeni Mezun','Yeni Mezun'),
        ('1-4 Yıl Tecrübeli','1-4 Yıl Tecrübeli'),
        ('5-9 Yıl Tecrübeli','5-9 Yıl Tecrübeli'),
        ('10+ Yıl Tecrübeli','10+ Yıl Tecrübeli'),
        ('Uzman','Uzman'),
    )
    status = models.CharField(max_length=150, blank=False, null=False, choices=status_choices)
    cv = models.FileField(upload_to=file_path, blank=True, null=True)
    notes = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name
