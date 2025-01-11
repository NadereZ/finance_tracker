from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from .models import Profile
from django.contrib.auth import logout

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in after successful registration
            messages.success(request, "Registration successful!")
            return redirect('homepage') # Redirect to the home page or any other page
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
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Login the user
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('tracker:dashboard') # Redirect to a home page or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    # Fetch the profile of the logged-in user
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'profile': user_profile,
    }
    return render(request, 'users/profile.html', context)

def user_logout(request):
    if request.method == 'POST':
        logout(request)  # Log out the user
        return redirect('homepage')  # Redirect to the homepage after logout
    return render(request, 'users/logout_confirmation.html')  # Render the confirmation page