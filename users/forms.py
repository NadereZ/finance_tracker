from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

# User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birthdate', 'profile_picture']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }


# User Profile Update Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birthdate', 'profile_picture']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }


# Login Form (optional customization)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
