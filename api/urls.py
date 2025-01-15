from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/', views.TransactionDetailView.as_view(), name='transaction-detail-view'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/', views.CategoryDetailView.as_view(), name='category-detail-view'),
    path('budget/', views.BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budget/', views.BudgetDetailView.as_view(), name='budget-detail-view'),
]

