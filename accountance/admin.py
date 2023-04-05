from django.contrib import admin

from .models import *

class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceLineInline,
    ]

admin.site.register(Invoice, FeedAdmin)
admin.site.register(Balance)
admin.site.register(Income)
admin.site.register(Expense)