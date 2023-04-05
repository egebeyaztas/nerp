from django.db import models
from django.db.models.signals import post_save, post_init
from general.models import Client
from scripts.keygen import KeyGenerator

keygenerator = KeyGenerator()

class Marketing(models.Model):
    social_media_marketing_reach = models.IntegerField(blank=True, null=True, default=0)
    social_media_marketing_clients = models.IntegerField(blank=True, null=True, default=0)
    mail_marketing_reach = models.IntegerField(blank=True, null=True, default=0)
    mail_marketing_clients = models.IntegerField(blank=True, null=True, default=0)
    organic_marketing_clients = models.IntegerField(blank=True, null=True, default=0)
    last_updated = models.DateTimeField(null=True, blank=True, auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        if self.last_updated:
            return 'Marketing Data - ' + str(self.last_updated)
        return 'Marketing Data - ' + str(self.created_at)

class PotentialClient(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    executive = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    notes = models.TextField(max_length=1200, blank=True, null=True)
    official = models.BooleanField(default=False)
    previous_state = None

    def __str__(self):
        return self.name

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        if instance.previous_state != instance.official:
            new_client = Client(
                name=instance.name,
                client_id=keygenerator.generate_unique_key('0'+str(instance.id)+'-'+instance.name[:2]+'-'),
                mail=instance.email,
                country=instance.location,
                representative_name=instance.executive,
            )
            new_client.save()
            instance.delete()

    @staticmethod
    def remember_state(sender, instance, **kwargs):
        instance.previous_state = instance.official

post_save.connect(PotentialClient.post_save, sender=PotentialClient)
post_init.connect(PotentialClient.remember_state, sender=PotentialClient)

class Ad(models.Model):
    platforms = (
        ('Facebook','Facebook'),
        ('Instagram','Instagram'),
        ('Google','Google'),
        ('Diğer','Diğer'),
    )
    platform = models.CharField(max_length=120, choices=platforms, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reached = models.IntegerField(blank=True, null=True, default=0)
    gained_clients = models.IntegerField(blank=True, null=True, default=0)
    cost = models.IntegerField(blank=True, null=True)
    on_air = models.BooleanField()
    on_air_for = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.platform + 'Reklamı No: ' + str(self.id)
"""
    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        if instance.previous_state != instance.on_air:
            instance.on_air_for = 

    @staticmethod
    def remember_state(sender, instance, **kwargs):
        instance.previous_state = instance.on_air

post_save.connect(PotentialClient.post_save, sender=PotentialClient)
post_init.connect(PotentialClient.remember_state, sender=PotentialClient)
"""