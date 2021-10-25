from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Sum
from .models import AccountLedger
from .forms import AccountLedgerForm
from common.models import UserProfile


class UserListledgerView(ListView):
    template_name = 'accounts/user_list_account.html'
    paginate_by = 100
    model = UserProfile
    ordering = '-id'


# class AddUserLedger(FormView):
#     form_class = AccountLedgerForm
#     template_name = 'customer/add_customer.html'

#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('common:login'))

#         return super(
#             AddCustomer, self).dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         form.save()
#         return HttpResponseRedirect(reverse('account:user_list_ledger'))

#     def form_invalid(self, form):
#         return super(AddCustomer, self).form_invalid(form)


class UserLedgerListView(ListView):
    model = AccountLedger
    template_name = 'accounts/user_list_ledger.html'
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            UserLedgerListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset
        account= AccountLedger.objects.filter(user=self.kwargs.get('pk'))
        if not queryset:
            queryset = self.model.objects.filter(
                user__id=self.kwargs.get('pk')).order_by('-dated')

        if self.request.GET.get('date'):
            queryset = queryset.filter(
                dated__icontains=self.request.GET.get('date')
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            UserLedgerListView, self).get_context_data(**kwargs)

        try:
            user = UserProfile.objects.get(id=self.kwargs.get('pk'))
        except UserProfile.DoesNotExist:
            raise Http404('user does not exits!')

        get_total_ledger_amnt = AccountLedger.objects.filter(user=self.kwargs.get('pk'))

        if get_total_ledger_amnt:
            ledger_debit = get_total_ledger_amnt.aggregate(Sum('debit_amount'))
            ledger_credit = get_total_ledger_amnt.aggregate(Sum('credit_amount'))

            debit_amount = ledger_debit.get('debit_amount__sum')
            credit_amount = ledger_credit.get('credit_amount__sum')

            total_remaining_amount = debit_amount - credit_amount
        else:
            debit_amount = 0
            credit_amount = 0
        context.update({
            'user': user,
            'debit_amount': debit_amount,
            'credit_amount': credit_amount,
            'total_remaining_amount':total_remaining_amount
        })
        return context


class DebitAccountLedgerFormView(FormView):
    template_name = 'accounts/debit.html'
    form_class = AccountLedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DebitAccountLedgerFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('accounts:user_ledger_list',
                    kwargs={'pk': obj.user.id}
                    )
        )

    def get_context_data(self, **kwargs):
        context = super(
            DebitAccountLedgerFormView, self).get_context_data(**kwargs)
        try:
            user = UserProfile.objects.get(id=self.kwargs.get('pk'))
        except UserProfile.DoesNotExist:
            raise Http404('UserProfile does not exits!')

        context.update({
            'user': user
        })
        return context


class CreditUserLedgerFormView(DebitAccountLedgerFormView):
    template_name = 'accounts/credit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CreditUserLedgerFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            CreditUserLedgerFormView, self).get_context_data(**kwargs)
        try:
            user = UserProfile.objects.get(id=self.kwargs.get('pk'))
        except UserProfile.DoesNotExist:
            raise Http404('UserProfile does not exits!')

        context.update({
            'user': user
        })
        return context