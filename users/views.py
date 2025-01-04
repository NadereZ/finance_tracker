from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in after successful registration
            messages.success(request, "Registration successful!")
            return redirect('home') # Redirect to the home page or any other page
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
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home') # Redirect to the home page
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})