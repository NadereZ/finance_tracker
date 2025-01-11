from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListCreateView, name='transaction-list-create'),
    path('transactions/', views.TransactionDetailView, name='transaction-detail-view'),
    path('categories/', views.CategoryListCreateView, name='category-list-create'),
    path('categories/', views.CategoryDetailView, name='category-detail-view'),
    path('budget/', views.BudgetListCreateView, name='budget-list-create'),
    path('budget/', views.BudgetDetailView, name='budget-detail-view'),
]

