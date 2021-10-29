from .views import IndexView, LoginView, LogoutView, UserListView, RegisterView
from django.urls import path
from common.reports_views import ReportsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('list/user/', UserListView.as_view(), name='user_list'),
    path('user/registration/form/', RegisterView.as_view(), name='register'),
    path('sales/reports/', ReportsView.as_view(), name='reports'),
]
