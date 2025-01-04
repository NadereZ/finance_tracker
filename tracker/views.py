from django.shortcuts import render, redirect
from .forms import TransactionForm, CategoryForm, BudgetForm
from .models import Transaction, Category, Budget
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Transaction


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

def transaction_list(request):
    transaction_list = Transaction.objects.all() # Fetch all transactions
    paginator = Paginator(transaction_list, 10) # 10 transactions per page

    page_number = request.GET.get('page') # Get the page number from the URL
    page_obj = paginator.get_page(page_number) # Get the page object

    return render(request, 'tracker/transaction_list.html', {'page_obj': page_obj})

# Homepage view
def homepage(request):
    return render(request, 'homepage.html')

# About page view
def about(request):
    return render(request, 'about.html')

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Get Started page view
def get_started(request):
    return render(request, 'get_started.html')