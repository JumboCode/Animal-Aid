from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from .models import Dog
from django.core.exceptions import PermissionDenied, EmptyResultSet
from core.models import Dog, Walker
from json import dumps

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
        if dog.get_visible():
            dog_info = {}
            dog_info["name"] = dog.name
            # temp fix until we can display images reliably
            dog_info["image_path"] = ''#dog.image.url 
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

def dog_list(request):
    # only able to view master list if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:
        # get all dogs in db
        dogs = Dog.objects.all()
        data = {'dogs':[]}
        # for each dog populate a dictionary w/ name, img, location, and db id
        for dog in dogs:
            data['dogs'].append({
                'name': dog.get_name,
                'image': dog.get_image,
                'location': dog.get_location,
                'id': dog.id,
            })
        return render(request, 'core/dog_list.html', data) 
    else:
        raise PermissionDenied()

# constants to change walking days and times
# Sizes should match DAYS and HOURS constants in core/models.py
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
HOURS = ['9:00am', '10:00am', '11:00am', '12:00pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm', '5:00pm']

def edit_dog(request):
    # only able to edit dogs if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:

        # get dog with id matchin=g url parameter
        dog_name = request.GET.get('q', '')

        # redirect back to list if id doesn't exist in db
        if not Dog.objects.filter(id=dog_name).exists():
            return redirect('dog_list')
        selected_dog = Dog.objects.get(id=dog_name)

        # POST request
        if request.method == 'POST':

            # save dog info if save button is pressed
            if 'save_dog' in request.POST:
                # assigning name, location, and zip from POST request
                selected_dog.name = request.POST.get('dog_name')
                selected_dog.location = request.POST.get('dog_location')
                selected_dog.zip_code = request.POST.get('dog_zip')
                selected_dog.visible = request.POST.get('dog_visible') == 'on'

                # assigning times from POST using checkbox id convention: "Thursday-2:00pm"
                chosen_times = []
                for day in DAYS:
                    for hour in HOURS:
                        chosen_times.append(request.POST.get(day + '-' + hour) == 'on')
                selected_dog.times = chosen_times

                selected_dog.save()

            # delete dog entry if delete button is pressed
            elif 'delete' in request.POST:
                selected_dog.delete()

            return redirect('dog_list')
        else:
            # two dictionaries passed to render:
            #   data: used by django framework to format walk times table
            #   json_data: used by js to display all stored walk times
            data = {
                'dog': {
                    'name': selected_dog.get_name,
                    'image': selected_dog.get_image,
                    'location': selected_dog.get_location,
                    'zip': selected_dog.get_zip,
                },
                'days': DAYS,
                'hours': HOURS,
            }
            json_data = {
                'days': DAYS,
                'hours': HOURS,
                'visible': selected_dog.get_visible(),
                'times': selected_dog.get_walktimes(),
            }
            return render(request, 'core/edit_dog.html', {'data':data, 'json_data':dumps(json_data)})
    else:
        # permission denied if user isn't staff
        raise PermissionDenied()

def add_dog(request):
    # only able to add dogs if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:

        # POST request
        if request.method == 'POST':

            if 'save_dog' in request.POST:
                # assigning name, location, and zip from POST request
                name_in = request.POST.get('dog_name')
                location_in = request.POST.get('dog_location')
                zip_code_in = request.POST.get('dog_zip')
                visible_in = request.POST.get('dog_visible') == 'on'

                # assigning times from POST using checkbox id convention: "Thursday-2:00pm"
                chosen_times = []
                for day in DAYS:
                    for hour in HOURS:
                        chosen_times.append(request.POST.get(day + '-' + hour) == 'on')
                
                new_dog = Dog(
                    name=name_in,
                    location=location_in,
                    zip_code=zip_code_in,
                    visible=visible_in,
                    times=chosen_times,
                    image='',
                )

                new_dog.save()
            
            return redirect('dog_list')
        else:
            data = {
                'days': DAYS,
                'hours': HOURS,
            }
            return render(request, 'core/add_dog.html', data)
    else:
        # permission denied if user isn't staff
        raise PermissionDenied()

# TODO staff needs to be able to change this number
PREF_COUNT = 5

def edit_walker(request):
    # only able to edit walker profile if logged in as a normal user, not staff
    if request.user.is_authenticated and not request.user.is_staff:
        
        username = request.user.get_username()

        # gets walker db entry if it already exists
        if Walker.objects.filter(email=username).exists():
            walker = Walker.objects.get(email=username)
        
        # creates a matching walker entry if one doesn't already exist
        else:
            walker = Walker(
                name='',
                email=username,
            )
            walker.save()

        name = walker.get_name()
        email = walker.get_email()
        phone_number = walker.get_phone_number()
        if phone_number == None:
            phone_number = ''

        # POST request
        if request.method == 'POST':

            # only save if save button was pressed
            if 'save_walker' in request.POST:

                # getting walker info from request
                walker.name = request.POST.get('walker_name')
                walker.phone_number = request.POST.get('walker_phone')

                # iterate through checkboxes to fill out chosen_times
                chosen_times = []
                for day in DAYS:
                    for hour in HOURS:
                        chosen_times.append(request.POST.get(day + '-' + hour) == 'on')
                walker.chosen_times = chosen_times

                # iterate through dog preferences to fill out dog_choices
                dog_choices = []
                for choice_num in range(PREF_COUNT):
                    dropdown_choice = request.POST.get(f'dog_select_{choice_num + 1}')

                    # append chosen dog name to dog_choices
                    if Dog.objects.filter(name=dropdown_choice).exists():
                        dog_choices.append(Dog.objects.get(name=dropdown_choice).get_name())
                        
                    # if '----' is chosen for a dog pref, then the pref is saved as None
                    else:
                        dog_choices.append(None)
                walker.dog_choices = dog_choices

                walker.save()

            # redirect to home if cancel button is pressed
            elif 'cancel' in request.POST:
                return redirect('home')

        # getting dog names to display in pref dropdowns
        all_dogs = Dog.objects.all()
        visible_dog_names = []
        for dog in all_dogs:
            if dog.get_visible(): # only displaying dogs which have visible = True
                visible_dog_names.append(dog.get_name())
        
        # helper array for Django template to loop through
        pref_nums = range(1, PREF_COUNT+1)

        data = {
            'walker': {
                'name': name,   
                'email': email,
                'phone': phone_number,
            },
            'days': DAYS,
            'hours': HOURS,
            'saved': (request.method == 'POST'),
            'dog_names': visible_dog_names,
            'pref_nums': pref_nums,
        }
        json_data = {
            'days': DAYS,
            'hours': HOURS,
            'times': walker.get_walktimes(),
            'dog_choices': walker.get_dog_choices(),
        }
        return render(request, 'core/edit_walker.html', {'data':data, 'json_data':dumps(json_data)})
    else:
        raise PermissionDenied()
