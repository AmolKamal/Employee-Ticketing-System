from django.urls import path
from . import views

urlpatterns = [
    path('raise-complaint/', views.raise_complaint, name='raise_complaint'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('view-tickets/', views.view_tickets, name='view_tickets'),
]