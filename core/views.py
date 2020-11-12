from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from .models import Dog

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

def dog_gallery(request):
    '''
       render (req, webpage, context)
       dictionary of {'dogs' : [dog_info] }
       DogInfo 'struct': name, pic (path to image)
       Getting dog info: import Dog model, do some querying of the db
    '''
    dogs = Dog.objects.all()
    dog_infos = []
    for dog in dogs:
        dog_info = {}
        dog_info["name"] = dog.name
        dog_info["image_path"] = dog.image.path 
        dog_infos.append(dog_info)
    
    return render(request, 'core/dog.html', {'dogs': dog_infos})
    
