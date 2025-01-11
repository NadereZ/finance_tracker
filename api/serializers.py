from rest_framework import serializers
from tracker.models import Transaction, Category, Budget
from users.models import CustomUser

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BudgetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'