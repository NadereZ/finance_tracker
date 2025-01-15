from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from tracker.models import Transaction, Category, Budget
from users.models import CustomUser

# Create your tests here.

class APITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name='Test Category'
        )
        
        # Create a test budget
        self.budget = Budget.objects.create(
            name='Test Budget',
            amount=1000.00,
            category=self.category
        )
        
        # Create a test transaction
        self.transaction = Transaction.objects.create(
            amount=100.00,
            type='income',
            category=self.category,
            description='Test Transaction'
        )
    def test_transaction_list_create(self):
        # Test GET request to list transactions
        url = reverse('transaction-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the created transaction is returned

        # Test POST request to create a new transaction
        data = {
            'amount': 200.00,
            'type': 'expense',
            'category': self.category.id,
            'description': 'New Test Transaction'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)  # Check if the transaction was created

    def test_transaction_detail(self):
        # Test GET request to retrieve a transaction
        url = reverse('transaction-detail', args=[self.transaction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Transaction')

        # Test PUT request to update a transaction
        data = {
            'amount': 150.00,
            'type': 'income',
            'category': self.category.id,
            'description': 'Updated Test Transaction'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated Test Transaction')

        # Test DELETE request to delete a transaction
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)  # Check if the transaction was deleted
    
    def test_category_list_create(self):
        # Test GET request to list categories
        url = reverse('category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the created category is returned

        # Test POST request to create a new category
        data = {
            'name': 'New Test Category'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Check if the category was created

    def test_category_detail(self):
        # Test GET request to retrieve a category
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

        # Test PUT request to update a category
        data = {
            'name': 'Updated Test Category'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Category')

        # Test DELETE request to delete a category
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  # Check if the category was deleted

    def test_budget_list_create(self):
        # Test GET request to list budgets
        url = reverse('budget-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the created budget is returned

        # Test POST request to create a new budget
        data = {
            'name': 'New Test Budget',
            'amount': 2000.00,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 2)  # Check if the budget was created

    def test_budget_detail(self):
        # Test GET request to retrieve a budget
        url = reverse('budget-detail', args=[self.budget.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Budget')

        # Test PUT request to update a budget
        data = {
            'name': 'Updated Test Budget',
            'amount': 1500.00,
            'category': self.category.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Budget')

        # Test DELETE request to delete a budget
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Budget.objects.count(), 0)  # Check if the budget was deleted


