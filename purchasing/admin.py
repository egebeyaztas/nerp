from django.contrib import admin
from .models import PurchaseOffer, PurchaseOfferLine

class OrderLineInline(admin.TabularInline):
    model = PurchaseOfferLine


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineInline,
    ]


admin.site.register(PurchaseOffer, FeedAdmin)
