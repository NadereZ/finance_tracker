from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile, UserPreference
from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm

# Create your tests here.

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        # Create a user
        user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Check if the user was created successfully
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_profile(self):
        # Create a profile
        profile = Profile.objects.create(
            user=self.user,
            bio='Test Bio',
            phone_number='1234567890',
            location='Test Location'
        )
        
        # Check if the profile was created successfully
        self.assertEqual(profile.bio, 'Test Bio')
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.location, 'Test Location')
class UserPreferenceModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_user_preference(self):
        # Create user preferences
        preference = UserPreference.objects.create(
            user=self.user,
            currency='EUR',
            dark_mode=True
        )
        
        # Check if the preferences were created successfully
        self.assertEqual(preference.currency, 'EUR')
        self.assertTrue(preference.dark_mode)

class CustomUserCreationFormTest(TestCase):
    def test_valid_user_creation_form(self):
        # Test valid form data
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'birthdate': '2000-01-01',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_creation_form(self):
        # Test invalid form data (missing required fields)
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomUserChangeFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_valid_user_change_form(self):
        # Test valid form data
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'birthdate': '2000-01-01'
        }
        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_user_change_form(self):
        # Test invalid form data (missing required fields)
        form_data = {
            'username': '',
            'email': 'updated@example.com',
            'birthdate': '2000-01-01'
        }
        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())


class CustomAuthenticationFormTest(TestCase):
    def test_valid_login_form(self):
        # Test valid form data
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        # Test invalid form data (missing required fields)
        form_data = {
            'username': '',
            'password': 'testpassword123'
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterViewTest(TestCase):
    def setUp(self):
        # Set up the client
        self.client = Client()

    def test_register_view(self):
        # Test GET request
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'birthdate': '2000-01-01',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('users:register'), form_data)
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful registration
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())  # Check if the user was created



class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Set up the client
        self.client = Client()

    def test_login_view(self):
        # Test GET request
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('users:login'), form_data)
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful login

class UpdateProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Set up the client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')

    def test_update_profile_view(self):
        # Test GET request
        response = self.client.get(reverse('users:update_profile'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'birthdate': '2000-01-01'
        }
        response = self.client.post(reverse('users:update_profile'), form_data)
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')  # Check if the username was updated