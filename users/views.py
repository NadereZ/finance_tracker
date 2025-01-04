from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in after successful registration
            messages.success(request, "Registration successful!")
            return redirect('homepage.html') # Redirect to the home page or any other page
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# User Profile Update View
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile') # Redirect to the user's profile page
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})

# User Login View

class CustomLoginView(LoginView):
    template_name = 'users/login.html' # Specify your custom login template

    def get_success_url(self):
        return reverse_lazy('dashboard') # Redirects to the dashboard view after login