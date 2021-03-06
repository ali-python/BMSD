from __future__ import unicode_literals
from django.contrib import admin
from .models import Invoice, InvoiceNotification


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__','bill_no', 'dho', 'hospital_name',
        'area', 'district', 'date', 'status_for_accepted'
    )
    search_fields = (
        'bill_no', 'dho__user__username',
    )
    
    @staticmethod
    def dho(obj):
        return obj.user.username if obj.customer else ''

class InvoiceNotificationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__','dho', 'invoice_dho', 'dated'
    )

    @staticmethod
    def dho(obj):
        return obj.dho.username if obj.dho else ''

admin.site.register(InvoiceNotification, InvoiceNotificationAdmin)
admin.site.register(Invoice, InvoiceAdmin)
