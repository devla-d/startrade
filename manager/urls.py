from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name="admin-dashboard"),
    path('users/', views.admin_dashboard_users_view, name="admin-dashboard-users"),
    path('payments/', views.admin_dashboard_pop_view, name="admin-dashboard-pop"),
    path('payments-approve/', views.admin_dashboard_approve_pop_view, name="admin-dashboard-pop-approve"),
    path('payments-decline/', views.admin_dashboard_decline_pop_view, name="admin-dashboard-pop-decline"),
    path('payments/<int:pk>/', views.admin_dashboard_pop_detail_view, name="admin-dashboard-pop-detail"),

]
