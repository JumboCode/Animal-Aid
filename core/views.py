from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from core.models import Dog

def home(request):
    return render(request, 'core/home.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Validate user login credentials.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    # If user did not enter the correct username and password combination,
    # or are visiting the page for the time, load default login form.
    form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
    
def results(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # database logic
            dogs = Dog.objects.all()
            data = {'matches':[]}
            for dog in dogs:
                data['matches'].append({
                    'name': dog.get_name,
                    'image': dog.get_image,
                    'location': dog.get_location,
                    'times': dog.get_walktimes,
                })
            return render(request, 'core/results.html', data)
        else:
            # GET req to load page
            return render(request, 'core/results.html')
    else:
        raise PermissionDenied()