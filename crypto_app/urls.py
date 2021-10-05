from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('packages/', views.packages_view, name='packages'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('investments/', views.investments_view, name='investments'),
    path('new-investments/', views.create_investments_view, name='new-investments-c'),
    path('new-investments/payment/complete/', views.create_investments_payment_view, name='new-investments-payment'),
    path('new-investments/checkout/', views.create_investments_payment_checkout_view, name='new-investments-checkout'),
    path('credit-user-invstments/', views.credit_daily_earning, name='credit-user'),
    path('end-user-invstments/', views.end_user_investment_view, name='end-investment'),
]
