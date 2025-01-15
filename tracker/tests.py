from django.test import TestCase, Client
from tracker.models import Category, Transaction, Budget
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from tracker.forms import TransactionForm,CategoryForm, BudgetForm 
from django.urls import reverse

# Create your tests here.


class CategoryModelTest(TestCase):
    def test_create_category(self):
        # Create a category
        category = Category.objects.create(name='Test Category')
        
        # Check if the category was created successfully
        self.assertEqual(category.name, 'Test Category')
        self.assertIsNotNone(category.created_at)


class TransactionModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category')

    def test_create_transaction(self):
        # Create a transaction
        transaction = Transaction.objects.create(
            user=self.user,
            amount=100.00,
            category=self.category,
            description='Test Transaction',
            transaction_type='income'
        )
        
        # Check if the transaction was created successfully
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(transaction.transaction_type, 'income')
        self.assertEqual(transaction.category.name, 'Test Category')

class BudgetModelTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name='Test Category')

    def test_create_budget(self):
        # Create a budget
        budget = Budget.objects.create(
            category=self.category,
            amount=1000.00,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30)
        )
        
        # Check if the budget was created successfully
        self.assertEqual(budget.amount, 1000.00)
        self.assertEqual(budget.category.name, 'Test Category')

class TransactionFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category')

    def test_valid_transaction_form(self):
        # Test valid form data
        form_data = {
            'amount': 100.00,
            'category': self.category.id,
            'description': 'Test Transaction',
            'transaction_type': 'income'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_transaction_form(self):
        # Test invalid form data (missing required fields)
        form_data = {
            'amount': 100.00,
            'category': self.category.id,
            'transaction_type': 'income'
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())


class CategoryFormTest(TestCase):
    def test_valid_category_form(self):
        # Test valid form data
        form_data = {'name': 'Test Category'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_category_form(self):
        # Test invalid form data (missing required fields)
        form_data = {}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())


class BudgetFormTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name='Test Category')

    def test_valid_budget_form(self):
        # Test valid form data
        form_data = {
            'category': self.category.id,
            'amount': 1000.00,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=30)
        }
        form = BudgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_budget_form(self):
        # Test invalid form data (missing required fields)
        form_data = {
            'category': self.category.id,
            'amount': 1000.00,
            'start_date': datetime.now()
        }
        form = BudgetForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddTransactionViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category')
        
        # Set up the client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_transaction(self):
        # Test GET request
        response = self.client.get(reverse('tracker:add_transaction'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        form_data = {
            'amount': 100.00,
            'category': self.category.id,
            'description': 'Test Transaction',
            'transaction_type': 'income'
        }
        response = self.client.post(reverse('tracker:add_transaction'), form_data)
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful submission
        self.assertEqual(Transaction.objects.count(), 1)  # Check if the transaction was created

class TransactionListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test category
        self.category = Category.objects.create(name='Test Category')
        
        # Create a test transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=100.00,
            category=self.category,
            description='Test Transaction',
            transaction_type='income'
        )
        
        # Set up the client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_transaction_list(self):
        # Test GET request
        response = self.client.get(reverse('tracker:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Transaction')  # Check if the transaction is in the response