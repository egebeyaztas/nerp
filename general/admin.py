from django.contrib import admin

from .models import *

class OrderLineInline(admin.TabularInline):
    model = OrderLine


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineInline,
    ]

admin.site.register(Order, FeedAdmin)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(StockGroup)
admin.site.register(Stock)
admin.site.register(Supplier)
