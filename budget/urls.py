from .views import (AddNewBudget, BudgetListView, BudgetUtilizeTemplateView, GenerateBudgetDistrictAPIView,
                    BudgetDetailListView, RevisedBudget,ReviseBudgetListView )
from django.urls import path

urlpatterns = [

     path('add/new/', AddNewBudget.as_view(), name='create_new_budget'),
     path('list/', BudgetListView.as_view(), name='list_budget'),
     path('list/detail/<int:pk>/', BudgetDetailListView.as_view(), name='list_budget_detail'),
     path('revised/district/<int:pk>/', RevisedBudget.as_view(), name='revised_budget'),
     path('revised/district/list/', ReviseBudgetListView.as_view(), name='revised_list'),
     path('utilize/district/<int:pk>/', BudgetUtilizeTemplateView.as_view(), name='budget_utilize'),
     path('generate/district/api/', GenerateBudgetDistrictAPIView.as_view(), name='generate_budget'),
]
