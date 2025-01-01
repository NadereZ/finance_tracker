from django.contrib import admin
from .models import Category, Transaction, Budget

# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['description', 'category__name', 'transaction_type']
    list_filter = ['transaction_type', 'category']
    list_display = ['date', 'amount', 'transaction_type', 'category', 'description']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(Budget)


