# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.utils import timezone
from invoice.models import Invoice

class ReportsView(TemplateView):
    template_name = 'reports.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ReportsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)

        sales = Invoice.objects.all()
        sales_sum = sales.aggregate(
            total_sales=Sum('grand_total')
        )

        today_sales = (
            Invoice.objects.filter(
                date__icontains=timezone.now().date()
            )
        )
        today_sales_sum = today_sales.aggregate(
            total_sales=Sum('grand_total')
        )

        context.update({
            'sales_count': sales.count(),
            'sales_sum': (
                int(sales_sum.get('total_sales')) if
                sales_sum.get('total_sales') else 0
            ),
            'today_sales_count': today_sales.count(),
            'today_sales_sum': (
                int(today_sales_sum.get('total_sales')) if
                today_sales_sum.get('total_sales') else 0
            )
        })

        return context
