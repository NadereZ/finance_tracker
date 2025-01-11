from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-budget/', views.add_budget, name='add_budget'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('categories/', views.category_list, name='category_list'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('update-transaction/<int:pk>/', views.update_transaction, name='update_transaction'),
    path('delete-transaction/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('dashboard/', views.dashboard, name='dashboard'),
]