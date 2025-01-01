from django.shortcuts import render, redirect
from .forms import TransactionForm, CategoryForm, BudgetForm
from .models import Transaction, Category, Budget
from django.shortcuts import get_object_or_404

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:transaction_list') # Redirect to the transaction list page after submission
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:category_list') # Redirect to the category list page after submission
    else:
        form = CategoryForm()
    return render(request, 'tracker/add_category.html', {'form': form})

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:budget_list') # Redirect to the budget list page after submission
    else:
        form = BudgetForm()
    return render(request, 'tracker/add_budget.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-data')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tracker/category_list.html', {'categories': categories})

def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})

def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('tracker:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/update_transaction.html', {'form': form})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('tracker:transaction_list')