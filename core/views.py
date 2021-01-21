from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from .models import Dog
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
        dog_info["image_path"] = dog.image.url if dog.image.url[-1] != "/" else dog.image.url[: - 1]
        dog_infos.append(dog_info)
    
    return render(request, 'core/dog.html', {'dogs': dog_infos})
    
def results(request):
    if request.user.is_authenticated and request.user.is_staff:

        # POST request
        if request.method == 'POST':
            # dog_query = request.POST.get('dog_select').value
            dog_query = request.POST.get("dog_select")
            
            # database logic
            dogs = Dog.objects.all()
            data = {'matches':[],
                    'dog_names':[] }

            """Return info of specific queried dog """
            # if we want all dogs, just add dogs to data
            if (dog_query == "All dogs"):
                for dog in dogs:
                    data['matches'].append({
                        'name': dog.get_name,
                        'image': dog.get_image,
                        'location': dog.get_location,
                        'times': dog.get_walktimes,
                    })
            
            # look for dog with name == dog query
            else:
                for dog in dogs:
                    if (str(dog) == dog_query):
                        data['matches'].append({
                            'name': dog.get_name,
                            'image': dog.get_image,
                            'location': dog.get_location,
                            'times': dog.get_walktimes,
                        })

            """Return names of all dogs for select dropdown """
            for dog in dogs:
                data['dog_names'].append({
                    'name': dog.get_name,
                })
            
            return render(request, 'core/results.html', data)
        
        # GET request
        else: 
            """Return names of all dogs for select dropdown """
            dogs = Dog.objects.all()
            data = {'dog_names':[]}
            for dog in dogs:
                data['dog_names'].append({
                    'name': dog.get_name,
                })
            return render(request, 'core/results.html', data) 
    else:
        raise PermissionDenied()
