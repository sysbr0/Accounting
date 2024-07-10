

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import CustomUser

# Create your views here.


def user(request):
    return render(request , 'base.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. You can now log in.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
    return render(request, 'register/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Replace 'index' with your desired redirect URL
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})



from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout




@login_required
def user_profile(request):
    return render(request, 'profile/profile.html', {'user': request.user})