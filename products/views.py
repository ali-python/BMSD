from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Sum
from .models import Company, Product, StockIn,StockOut, ProductDetail, PurchasedProduct
from .forms import (
    CompanyForm, ProductForm,StockInForm,StockOutForm)
from django.utils import timezone

class AddCompany(FormView):
    form_class = CompanyForm
    template_name = 'products/add_company.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddCompany, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:company_list'))

    def form_invalid(self, form):
        return super(AddCompany, self).form_invalid(form)

class CompanyList(TemplateView):
    template_name = 'products/company_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            CompanyList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompanyList, self).get_context_data(**kwargs)
        company = Company.objects.all()
        context.update({
            'company': company
        })
        return context

class ProductItemList(ListView):
    template_name = 'products/list_product.html'
    paginate_by = 100
    model = Product
    ordering = '-id'

    # def get_queryset(self):
    #     queryset = self.queryset
    #     if not queryset:
    #         queryset = Product.objects.all()

    #     queryset = queryset.filter(id=self.kwargs.get('id'))
    #     return queryset.order_by('-id')	


class AddNewProduct_list(FormView):
    form_class = ProductForm
    template_name = 'products/add_product.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            AddNewProduct_list, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.save()

        return HttpResponseRedirect(reverse('product:products_items_list'))

    def form_invalid(self, form):
    	print(form.errors)
    	print("_______________________________________")
    	print("_______________________________________")
    	print("_______________________________________")
    	return super(AddNewProduct_list, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewProduct_list, self).get_context_data(**kwargs)
        products = Product.objects.all()
        companies = Company.objects.all()
        context.update({
            'products': products,
            'companies': companies
        })
        return context


class StockInListView(ListView):
    template_name = 'products/stock_in_list.html'
    paginate_by = 100
    model = StockIn
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = StockIn.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('id'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(StockInListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('id'))
        })
        return context

class AddStockItems(FormView):
    template_name = 'products/stock_in.html'
    form_class = StockInForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))
        return super(AddStockItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        return HttpResponseRedirect(
            reverse('product:stock_items_list', kwargs={'id': product_item_detail.product.id})
                    )

    def form_invalid(self, form):
        return super(AddStockItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddStockItems, self).get_context_data(**kwargs)
        try:
            product = Product.objects.get(id=self.kwargs.get('id'))
            
        except ObjectDoesNotExist:
            raise Http404('Product not found !')

        context.update({
            'product': product
        })
        return context


class ProductUpdateView(UpdateView):
    template_name = 'products/product_update.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:products_items_list')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        companies = Company.objects.all()
        context.update({
            'companies': companies
        })
        return context