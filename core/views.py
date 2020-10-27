from django import forms
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def home(request):
    return render(request, 'core/home.html')

def login(request):
    print("Hello, World!")
    return render(request, 'core/login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
    
