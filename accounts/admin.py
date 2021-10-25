from django.contrib import admin

from .models import AccountLedger

class AccountLedgerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit_amount', 'credit_amount', 'details', 'status','dated'
    )
    search_fields = (
        'invoice__bill_no',
    )

    @staticmethod
    def invoice(obj):
        return obj.bill_no

admin.site.register(AccountLedger, AccountLedgerAdmin)

