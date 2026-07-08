from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("",views.homeView, name='home'),
    path('register/', views.register_employee, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/edit/<str:employee_id>/', views.admin_edit_employee, name='admin_edit_employee'),
    path('admin-panel/delete/<str:employee_id>/', views.admin_delete_employee, name='admin_delete_employee'),
]