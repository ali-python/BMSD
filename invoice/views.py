import json
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView, View, DeleteView
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Invoice, InvoiceNotification
from common.models import UserProfile
from products.models import StockIn, Product
from accounts.forms import AccountLedgerForm
from .forms import InvoiceForm, InvoiceNotificationForm
from products.forms import StockOutForm
from django.contrib.auth.models import User

from products.models import ProductFormula


class InvoiceListView(ListView):
    template_name = 'invoice/invoice_list.html'
    model = Invoice
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceListView, self).dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     queryset = self.queryset
    #     if not queryset:
    #         queryset = Invoice.objects.all().order_by('-id')

    #     if self.request.GET.get('customer_name'):
    #         queryset = queryset.filter(
    #             customer__name__contains=self.request.GET.get('customer_name'))

    #     if self.request.GET.get('customer_id'):
    #         queryset = queryset.filter(
    #             id=self.request.GET.get('customer_id').lstrip('0')
    #         )

    #     if self.request.GET.get('bill_no'):
    #         queryset = queryset.filter(
    #             bill_no=self.request.GET.get('bill_no')
    #         )

    #     if self.request.GET.get('date'):
    #         queryset = queryset.filter(
    #             date=self.request.GET.get('date')
    #         )

    #     return queryset.order_by('-id')


class CreateInvoiceTemplateView(TemplateView):
    template_name = 'invoice/create_invoice.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreateInvoiceTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateInvoiceTemplateView, self).get_context_data(**kwargs)
        context.update({
            'user': UserProfile.objects.all().order_by('id'),
            'p_f': ProductFormula.objects.all().order_by('id'),
            'products': StockIn.objects.all().order_by('id'),
            'today_date': timezone.now().date(),
        })
        return context


class ProductFormulaListAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ProductListAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        products = ProductFormula.objects.all()
        print(products)
        print("______________________________________")
        print("______________________________________")
        print("______________________________________")
        print("______________________________________")
        items = []

        for product in products:
            p = {
                'id': product.id,
                'name': product.product_name,
                'company':product.product_formula_name
            }

            if product.stockin_product.exists():
                stock_detail = product.stockin_product.all().latest('id')
                p.update({
                    'retail_price': stock_detail.price_per_item,
                    'consumer_price': stock_detail.price_per_item,
                    'expiry': stock_detail.stock_expiry,
                })

                all_stock = product.stockin_product.all()
                if all_stock:
                    all_stock = all_stock.aggregate(Sum('quantity'))
                    all_stock = float(all_stock.get('quantity__sum') or 0)
                else:
                    all_stock = 0

                purchased_stock = product.stockout_product.all()
                if purchased_stock:
                    purchased_stock = purchased_stock.aggregate(
                        Sum('stock_out_quantity'))
                    purchased_stock = float(
                        purchased_stock.get('stock_out_quantity__sum') or 0)
                else:
                    purchased_stock = 0

                p.update({
                    'stock': all_stock - purchased_stock
                })

            else:
                p.update(
                    {
                        'retail_price':0,
                        'consumer_price':0,
                        'expiry':0
                    }
                )

            items.append(p)

        return JsonResponse({'products': items})

class ProductListAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ProductListAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        print(products)
        print("______________________________________")
        print("______________________________________")
        print("______________________________________")
        print("______________________________________")
        items = []

        for product in products:
            p = {
                'id': product.id,
                'name': product.product_name,
                'company':product.company_name.name
            }

            if product.stockin_product.exists():
                stock_detail = product.stockin_product.all().latest('id')
                p.update({
                    'retail_price': stock_detail.price_per_item,
                    'consumer_price': stock_detail.price_per_item,
                    'expiry': stock_detail.stock_expiry,
                })

                all_stock = product.stockin_product.all()
                if all_stock:
                    all_stock = all_stock.aggregate(Sum('quantity'))
                    all_stock = float(all_stock.get('quantity__sum') or 0)
                else:
                    all_stock = 0

                purchased_stock = product.stockout_product.all()
                if purchased_stock:
                    purchased_stock = purchased_stock.aggregate(
                        Sum('stock_out_quantity'))
                    purchased_stock = float(
                        purchased_stock.get('stock_out_quantity__sum') or 0)
                else:
                    purchased_stock = 0

                p.update({
                    'stock': all_stock - purchased_stock
                })

            else:
                p.update(
                    {
                        'retail_price':0,
                        'consumer_price':0,
                        'expiry':0
                    }
                )

            items.append(p)

        return JsonResponse({'products': items})

class GenerateInvoiceAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        hospital_name = self.request.POST.get('hospital_name')
        district = self.request.POST.get('district')
        sub_total = self.request.POST.get('sub_total')
        discount = self.request.POST.get('discount')
        shipping = self.request.POST.get('shipping')
        grand_total = self.request.POST.get('grand_total')
        totalQty = self.request.POST.get('totalQty')
        remaining_payment = self.request.POST.get('remaining_amount')
        paid_amount = self.request.POST.get('paid_amount')
        cash_payment = self.request.POST.get('cash_payment')
        returned_cash = self.request.POST.get('returned_cash')
        dated = self.request.POST.get('dated')
        bill_no = self.request.POST.get('bill_no')
        items = json.loads(self.request.POST.get('items'))

        print(items)
        print("_____________________________")
        print("_____________________________")
        print("_____________________________")

        with transaction.atomic():
            invoice_form_kwargs = {
            	'district':district,
            	'hospital_name': hospital_name,
            	'dho':user_id,
                'bill_no': bill_no,
                'date': dated,
                'discount': float(discount),
                'sub_total': float(sub_total),
                'grand_total': float(grand_total),
                'total_quantity': totalQty,
                'shipping': float(shipping),
                'paid_amount': float(paid_amount),
                'remaining_payment': float(remaining_payment),
                'cash_payment': float(cash_payment),
                'returned_payment': float(returned_cash),
            }
            invoice_form = InvoiceForm(invoice_form_kwargs)
            invoice = invoice_form.save(commit=False)
            invoice_form.save()

            for item in items:
            	print(item.get('item_id'))
            	print("_____________________it__________________")
            	print("_____________________it__________________")
            	print("_____________________it__________________")

            for item in items:
                product = StockIn.objects.get(product__product_name=item.get('item_name'))
                latest_stockin = StockIn.objects.all().latest('id')
                stock_out_kwargs = {
                    'product': product.id,
                    'invoice': invoice.id,
                    'selling_price': (
                            float(item.get('price'))),
                    'stock_out_quantity': totalQty,
                    'dated': timezone.now().date()
                }
                stock_out = StockOutForm(stock_out_kwargs)
                stock_out.save()
                product.save()
            print("_______________________ur___________________")
            print("_______________________ur___________________")
            print("_______________________ur___________________")
            print(self.request.POST.get(user_id))
            user = User.objects.get(id=user_id)
            if user or self.request.POST.get('user_id'):
                if float(grand_total):
                    ledger_form_kwargs = {
                        'user': user,
                        'debit_amount': float(grand_total),
                        'details': (
                                'Payment for Bill/Receipt No %s '
                                % str(invoice.id).zfill(7)),
                        'dated': timezone.now()
                    }

                    user_ledger = AccountLedgerForm(ledger_form_kwargs)
                    user_ledger.save()
            invoice_notificatfion_form_kwargs = {
                'dho':user_id,
                'invoice_dho': invoice.id,
            }
            invoice_notification_form = InvoiceNotificationForm(invoice_notificatfion_form_kwargs)
            invoice_notify = invoice_notification_form.save(commit=False)
            invoice_notification_form.save()

        return JsonResponse({'invoice_id': invoice.id})


class InvoiceDetailTemplateView(TemplateView):
    template_name = 'invoice/invoice_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceDetailTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailTemplateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'invoice': invoice
        })
        return context


class DeleteInvoice(DeleteView):
    model = Invoice
    success_url = reverse_lazy('japan_inventory:invoice_list')
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DeleteInvoice, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class InvoiceNotificationListView(ListView):
    template_name = 'invoice/invoice_notification_list.html'
    model = InvoiceNotification
    paginate_by = 100
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            InvoiceNotificationListView, self).dispatch(request, *args, **kwargs)


class ConfirmInvoiceAPIView(View):

    def post(self, request, *args, **kwargs):
        print("______________-comg____________________")
        print("______________-comg____________________")
        print("______________-comg____________________")
        print("______________-comg____________________")
        print("______________-comg____________________")
        invoice = Invoice.objects.get(id=self.request.POST.get('invoice_id'))
        invoice.status_for_accepted = 'True'
        invoice.save()

        return JsonResponse({
            'status': True,
        })
