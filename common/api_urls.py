from django.urls import path


from common.api_views import DailySalesAPI, WeeklySalesAPI, MonthlySalesAPI

urlpatterns = [
    path('sales/daily/', DailySalesAPI.as_view(),name='daily_sales_api'),
    path('sales/weekly/', WeeklySalesAPI.as_view(),name='weekly_sales_api'),
    path('sales/monthly/', MonthlySalesAPI.as_view(),name='monthly_sales_api'),

]
