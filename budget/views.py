from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from calendar import monthrange
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, RedirectView, UpdateView, ListView, View
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
import json
from django.http import HttpResponseRedirect,HttpResponse
from django.db import transaction
from django.contrib.auth import authenticate
from .forms import BmsdBudgetForm, BudgetUtilizeDistrictForm, ReviseBudgetDistrictForm
from .models import BmsdBudget, BudgetUtilizeDistrict, ReviseBudgetDistrict
from common.models import District, UserProfile
from django.contrib.auth.models import User



class BudgetListView(ListView):
    template_name = 'budget/budget_list.html'
    paginate_by = 100
    model = BmsdBudget
    ordering = '-id'


class AddNewBudget(FormView):
    form_class = BmsdBudgetForm
    template_name = 'budget/create_new_budget.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddNewBudget, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('budget:list_budget'))

    def form_invalid(self, form):
        return super(AddNewBudget, self).form_invalid(form)


class BudgetUtilizeTemplateView(TemplateView):
    template_name = 'budget/budget_utilize_district.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            BudgetUtilizeTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BudgetUtilizeTemplateView, self).get_context_data(**kwargs)
        district = District.objects.all()
        budget = BmsdBudget.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'district': district,
            'budget':budget
        })
        return context

class GenerateBudgetDistrictAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            GenerateBudgetDistrictAPIView, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateBudgetDistrictAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        utilize_total_budget = self.request.POST.get('utilize_total_budget')
        start_dated = self.request.POST.get('start_dated')
        end_dated = self.request.POST.get('end_dated')
        items = json.loads(self.request.POST.get('items'))
        user = UserProfile.objects.get(user__username=self.request.POST.get('username'))
        if user:
	        with transaction.atomic():
	            total_budget = BmsdBudget.objects.get(budget_amount=self.request.POST.get('utilize_total_budget'))
	            total_budget.status = True
	            total_budget.save()
	            # budget_utilize = BudgetUtilizeDistrict.objects.get(
	            # 	utilize_total_budget=total_budget)

	            for item in items:
	                budget_district = District.objects.get(name=item.get('district'))
	                b_u_d = BudgetUtilizeDistrict.objects.create(
	                	district=budget_district, utilize_total_budget=total_budget,
	                	start_dated=total_budget.start_dated, end_dated=total_budget.end_dated,
	                	discription='Fund from BMSD ', district_budget_amount=float(item.get('district_budget_amount')),
	                	dated=timezone.now().date(), status= True
	                	)
	                # budget_utilize_form_kwargs = {
	                #     'district': budget_district.id,
	                #     'utilize_total_budget':total_budget,
	                #     'start_dated':total_budget.start_dated,
	                #     'end_dated':total_budget.end_dated,
	                #     'discription': 'Fund from BMSD ',
	                #     'district_budget_amount': (
	                #             float(item.get('district_budget_amount'))),
	                #     'dated': timezone.now().date(),
	                #     'status': True
	                # }
	                # budget_ut = BudgetUtilizeDistrictForm(budget_utilize_form_kwargs)
	                # budget_ut.save()

	        return JsonResponse({'budget_id': b_u_d.id})
        else:
        	return JsonResponse({'Error': 'error'})

class BudgetDetailListView(ListView):
    template_name = 'budget/budget_detail.html'
    paginate_by = 100
    model = BudgetUtilizeDistrict
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = BudgetUtilizeDistrict.objects.all()

        queryset = queryset.filter(utilize_total_budget=self.kwargs.get('pk'))
        return queryset.order_by('-id')


class RevisedBudget(FormView):
    form_class = ReviseBudgetDistrictForm
    template_name = 'budget/revised_budget.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            RevisedBudget, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        revised_budget=form.save()
        revised_budget.previous_budget_record.district.name = self.request.POST.get('district')
        revised_budget.save()
        return HttpResponseRedirect(reverse('budget:list_budget'))

    def form_invalid(self, form):
    	print(form.errors)
    	return super(RevisedBudget, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(RevisedBudget, self).get_context_data(**kwargs)
        old_budget = BudgetUtilizeDistrict.objects.get(id=self.kwargs.get('pk'))
        print(old_budget.district.name)
        # for b in old_budget:
        # 	print(b.district.name)
        print("_______________________________")
        print("_______________________________")
        print("_______________________________")
        print("_______________________________")
        context.update({
            'old_budget': old_budget,
        })
        return context

class ReviseBudgetListView(ListView):
    template_name = 'budget/revise_budget_list.html'
    paginate_by = 100
    model = ReviseBudgetDistrict
    ordering = '-id'

    def get_queryset(self):
	    queryset = self.queryset
	    if not queryset:
	        queryset = ReviseBudgetDistrict.objects.all()

	    queryset = queryset
	    for q in queryset:
	    	print(q.previous_budget_record.utilize_total_budget.budget_amount)
	    	print(q.previous_budget_record.district.name)
	    	print(q.previous_budget_record.district_budget_amount)
	    return queryset.order_by('-id')



# class ReviseBudgetListView(TemplateView):
#     template_name = 'budget/budget_detail.html'

#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('common:login'))

#         return super(
#             ReviseBudgetListView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(ReviseBudgetListView, self).get_context_data(**kwargs)
#         budget = ReviseBudgetDistrict.objects.all()
#         for budget in budget:
#         	print(budget.previous_budget_record.utilize_total_budget.budget_amount)
#         context.update({
#             'budget': budget
#         })
#         return context

