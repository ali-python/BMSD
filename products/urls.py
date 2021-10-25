from django.urls import path
from .views import (ProductItemList, CompanyList, AddCompany, AddNewProduct_list, StockInListView,
					 AddStockItems, ProductUpdateView)


urlpatterns = [
	path('save/company/', AddCompany.as_view(), name='add_company'),
    path('list/company/', CompanyList.as_view(), name='company_list'),
    path('save/product/', AddNewProduct_list.as_view(), name='add_product'),
    path('list/products/items/', ProductItemList.as_view(), name='products_items_list'),
    path('list/stock/items/<int:id>/', StockInListView.as_view(), name='stock_items_list'),
    path('add/stock/items/<int:id>/', AddStockItems.as_view(), name='stock_items_add'),
    path('update/product/items/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    ]