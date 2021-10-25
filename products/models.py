from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
import random
from django.db.models.signals import post_save
from invoice.models import Invoice
from common.models import DatedModel
from django.utils import timezone


class Company(models.Model):
	name = models.CharField(max_length=100, unique=True)
	dated = models.DateField(default=timezone.now, null=True, blank=True)

class Product(models.Model):
    UNIT_TYPE_KG = 'Kilogram'
    UNIT_TYPE_GRAM = 'Gram'
    UNIT_TYPE_LITRE = 'Litre'
    UNIT_TYPE_QUANTITY = 'Quantity'

    UNIT_TYPES = (
        (UNIT_TYPE_KG, 'Kilogram'),
        (UNIT_TYPE_GRAM, 'Gram'),
        (UNIT_TYPE_LITRE, 'Litre'),
        (UNIT_TYPE_QUANTITY, 'Quantity'),
    )
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='company_name')
    unit_type = models.CharField(
        choices=UNIT_TYPES, default=UNIT_TYPE_QUANTITY,
        blank=True, null=True, max_length=200
    )
    product_name = models.CharField(max_length=100, unique=True)
    status_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    def total_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        return stock_in


    def product_available_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return  stock_in - stock_out

    def product_purchased_items(self):
        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return  stock_out

def int_to_bin(value):
        return bin(value)[2:]


def bin_to_int(value):
        return int(value, base=2)

class StockIn(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockin_product',on_delete=models.CASCADE
    )
    quantity = models.CharField(
        max_length=100, blank=True, null=True
    )
    price_per_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text="Selling Price for a Single Item"
    )
    total_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text='Buying Price for a Single Item'
    )
    total_buying_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    dated_order = models.DateField(blank=True, null=True)
    stock_expiry = models.DateField(blank=True, null=True)

    def __str__ (self):
        return self.product.product_name


class ProductDetail(DatedModel):
    product = models.ForeignKey(
        Product, related_name='product_detail',on_delete=models.CASCADE
    )
    retail_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
    )
    consumer_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
    )
    available_item = models.IntegerField(default=1)
    purchased_item = models.IntegerField(default=0)

    def __unicode__(self):
        return self.product.product_name


class PurchasedProduct(DatedModel):
    product = models.ForeignKey(
        Product, related_name='purchased_product',on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        Invoice, related_name='purchased_invoice',
        blank=True, null=True,on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=1, blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.product.product_name

class StockOut(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockout_product',on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        Invoice, related_name='invoice_stockout', blank=True, null=True, on_delete=models.CASCADE)
    purchased_item = models.ForeignKey(
        PurchasedProduct, related_name='out_purchased',
        blank=True, null=True,on_delete=models.CASCADE
    )
    stock_out_quantity=models.CharField(max_length=100, blank=True, null=True)
    selling_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    dated=models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.product.product_name


# Signals
def purchase_product(sender, instance, created, **kwargs):
    """
    TODO: Ali Please check this function is useful or not.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    product_items = (
        instance.product.product_detail.filter(
            available_item__gt=0).order_by('created_at')
    )

    if product_items:
        item = product_items[0]
        item.available_item - 1
        item.save()
