from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Invoice(models.Model):
    district = models.CharField(max_length=200, blank=True, null=True)
    area = models.CharField(max_length=200, blank=True, null=True)
    hospital_name = models.CharField(max_length=200, blank=True, null=True)
    dho = models.ForeignKey(
        User,
        related_name='dho',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    bill_no = models.CharField(max_length=10, blank=True, null=True)

    total_quantity = models.CharField(
        max_length=10, blank=True, null=True, default=1
    )

    sub_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    remaining_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    discount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    shipping = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    grand_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    cash_returned = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)
    status_for_accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id).zfill(7)

class InvoiceNotification(models.Model):
    dho = models.ForeignKey(
        User,
        related_name='dho_invoice',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    invoice_dho = models.ForeignKey(Invoice, related_name='invoices_notification', blank=True, null=True,
        on_delete=models.SET_NULL)
    dated = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return str(self.invoice_dho.id)