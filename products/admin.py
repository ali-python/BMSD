from __future__ import unicode_literals
from django.contrib import admin

from .models import Product, Company
from .models import ProductDetail
from .models import PurchasedProduct
from .models import StockIn,StockOut

class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name', 'dated')

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'product_name','UNIT_TYPE_QUANTITY',
        'quantity', 'retail_price', 'consumer_price'
    )
    search_fields = (
        'name', 'product_name','unit_type'
    )

    @staticmethod
    def quantity(obj):
        return 'under progress'

    @staticmethod
    def retail_price(obj):
        return 'under progress'

    @staticmethod
    def consumer_price(obj):
        return 'under progress'


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'product', 'retail_price',
        'consumer_price', 'available_item', 'purchased_item',
    )

    @staticmethod
    def product(obj):
        return obj.product.product_name

    @staticmethod
    def discount_amount(obj):
        return 'under_progress'

    @staticmethod
    def profit_amount(obj):
        return obj.consumer_price - obj.retail_price

    @staticmethod
    def remaining_item(obj):
        return obj.available_item - obj.purchased_item


class PurchasedProductAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'invoice_no', 'discount_percentage', 'created_at'
    )

    @staticmethod
    def invoice_no(obj):
        return obj.invoice.bill_no if obj.invoice else ''


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'product', 'quantity', 'price_per_item',
        'total_amount', 'dated_order','stock_expiry'
    )
    search_fields = ('product__name','stock_expiry','dated_order')

    @staticmethod
    def product(obj):
        return obj.product_name if obj.product_name else ''


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'product', 'invoice_no', 'stock_out_quantity', 'dated',
    )
    search_fields = ('product__name','stock_out_quantity','dated')

    @staticmethod
    def invoice_no(obj):
        return obj.invoice.bill_no if obj.invoice else ''

admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
