from django.urls import path
from .views import UserLedgerListView, DebitAccountLedgerFormView, CreditUserLedgerFormView, UserListledgerView 

urlpatterns = [
    path('list/user/ledger/', UserListledgerView.as_view(), name='user_list_ledger'),

    path(
        '<int:pk>/ledger/list/',
        UserLedgerListView.as_view(),
        name='user_ledger_list'
    ),
    path(
        '<int:pk>/ledger/debit/',
        DebitAccountLedgerFormView.as_view(),
        name='user_ledger_debit'
    ),
    path(
        '<int:pk>/ledger/credit/',
        CreditUserLedgerFormView.as_view(),
        name='user_ledger_credit'
    )

    ]