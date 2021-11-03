from django.urls import path
from .views import (
    InvoiceListView, CreateInvoiceTemplateView, ProductListAPIView,
    GenerateInvoiceAPIView, InvoiceDetailTemplateView, InvoiceNotificationListView, ConfirmInvoiceAPIView
)

urlpatterns = [
    path('list/invoice/', InvoiceListView.as_view(), name='invoice_list'),
    path('list/invoice/notification/', InvoiceNotificationListView.as_view(), name='invoice_list_notification'),
    path('add/invoice/user/', CreateInvoiceTemplateView.as_view(), name='add_invoice'),
    path('product/invoice/user/api/', ProductListAPIView.as_view(), name='product_api'),
    path('confirmation/api/', ConfirmInvoiceAPIView.as_view(), name='invoice_confirm_api'),
    path('generate/invoice/api/', GenerateInvoiceAPIView.as_view(), name='generate_invoice'),
    path("detail/<int:pk>/", InvoiceDetailTemplateView.as_view(), name='invoice_detail'),
]
