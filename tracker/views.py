from django.shortcuts import render, redirect
from .forms import TransactionForm, CategoryForm, BudgetForm
from .models import Transaction, Category, Budget
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Sum, Q
from datetime import datetime
from django.contrib.auth.decorators import login_required


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

@login_required
def dashboard(request):
    # Fetch recent transactions (last 10 entries)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]

    # Calculate current balance
    current_balance = Transaction.objects.filter(user=request.user).aggregate(
        balance=Sum('amount', filter=Q(transaction_type='income')) -
                Sum('amount', filter=Q(transaction_type='expense'))
    )['balance'] or 0

    # Calculate monthly spending
    monthly_spending = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__month=datetime.now().month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Budget utilization calculation
    budgets = Budget.objects.filter(category__transaction__user=request.user)
    budget_utilization = {
        budget.category.name: (Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0) / budget.limit * 100
        for budget in budgets
    }

    # Pass data to the template
    context = {
        'transactions': transactions,
        'current_balance': current_balance,
        'monthly_spending': monthly_spending,
        'budget_utilization': budget_utilization,
    }
    return render(request, 'tracker/dashboard.html', context)