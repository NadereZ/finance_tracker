from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default=EXPENSE)

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.amount}"
    
class Budget(models.Model):
    category = models.ForeignKey(Category, related_name='budgets', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.category.name} Budget: {self.amount} ({self.start_date} to {self.end_date})"
    
