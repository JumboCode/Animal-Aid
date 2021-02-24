from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from .models import Dog, Walker, Match
from django.core.exceptions import PermissionDenied
from core.models import Dog, Walker, Match

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
        dog_info["name"] = dog.get_name
        # dog_info["image_path"] = dog.image.url 
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
            data = {'match_results':[],
                    'dog_names':[] ,
                    'dog':[],
                    }
            # Return names of all dogs for select dropdown
            for dog in dogs:
                data['dog_names'].append({
                    'name': dog.get_name,
                })
            if (dog_query == "Select Dog"):
                return render(request, 'core/results.html', data)
            # Get dog objects based on query string
            dog_results = Dog.objects.filter(dog_name = dog_query)
            dog_result = dog_results[0] # Use the first dog
            # Find all matches associated with that dog
            matches = Match.objects.filter(dog = dog_result)
            # Send information about the dog and matches
            data['dog'].append({
                "name" : dog_result.get_name,
                "location" : dog_result.get_location,
                "owner" : dog_result.get_owner,
            })
            
            for match in matches:
                # print(type(match.get_time))
                walker_query = match.get_walker
                print(str(walker_query))
                # walker_results = Walker.objects.filter(walker = walker_query)
                # print(walker_results)
                # walker = walker_results[0]
                # print(walker)
                data["match_results"].append({
                    "dog" : match.get_dog,
                    "walker" : walker_query,
                    # "walker_email" : walker.get_email,
                    "day" : match.get_day,
                    "start_time" : match.get_start_time,
                    "end_time" : match.get_end_time,
                })
            return render(request, 'core/results.html', data)
        
        # GET request
        else: 
            # Return names of all dogs for select dropdown for initial page load
            dogs = Dog.objects.all()
            data = {
                "dog_names":[],
                "match_results" : []
            }
            for dog in dogs:
                data["dog_names"].append({
                    "name": dog.get_name,
                })
            return render(request, 'core/results.html', data) 
            
    else:
        raise PermissionDenied()
