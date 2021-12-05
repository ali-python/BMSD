from django.urls import path
from .views import (ProductItemList, CompanyList, AddCompany, AddNewProduct_list, StockInListView,
					 AddStockItems, ProductUpdateView, AddProductFormula, ProductFormulaList, AddRequestedProduct,
					 AvailableProductFormulaView, RequestForFormula)


urlpatterns = [
	path('save/company/', AddCompany.as_view(), name='add_company'),
    path('request/formula/dho/', RequestForFormula.as_view(), name='request_dho_formula'),
    path('list/product/formula/', ProductFormulaList.as_view(), name='product_formula_list'),
    path('list/available/formula/', AvailableProductFormulaView.as_view(), name='available_product_formula_list'),
    path('add/requested/formula/', AddRequestedProduct.as_view(), name='requested_formula'),
    path('add/formula/', AddProductFormula.as_view(), name='add_product_formula'),
    path('list/company/', CompanyList.as_view(), name='company_list'),
    path('save/product/', AddNewProduct_list.as_view(), name='add_product'),
    path('list/products/items/', ProductItemList.as_view(), name='products_items_list'),
    path('list/stock/items/<int:id>/', StockInListView.as_view(), name='stock_items_list'),
    path('add/stock/items/<int:id>/', AddStockItems.as_view(), name='stock_items_add'),
    path('update/product/items/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    ]