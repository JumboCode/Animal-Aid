from django import forms
from .forms import CustomUserCreationForm, LoginForm, S3DirectUploadForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from .models import Dog, Walker, Match
from django.core.exceptions import PermissionDenied, EmptyResultSet
from core.models import Dog, Walker, Match
from json import dumps
import random
from django.core.mail import send_mail

global form_is_open
form_is_open = False

SUBSCRIBE_RECIPIENT = 'Benjamin.London@tufts.edu'

# constants to change walking days and times
# Sizes should match DAYS and HOURS constants in core/models.py
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
HOURS = ['9:00am', '10:00am', '11:00am', '12:00pm', '1:00pm', '2:00pm', '3:00pm', '4:00pm', '5:00pm']

def home(request):
    if request.method == 'POST' and 'subscribe' in request.POST:
        email = request.POST.get('subscribeemail')
        send_mail(
            # subject line
            'Animal Aid Subscription Request',
            # body
            'The following email would like to subscribe to the Animal Aid mailing list:\n' + email,
            '',
            [SUBSCRIBE_RECIPIENT],
        )
        return redirect('home')
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
            return redirect('edit_walker')
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
        dog_info["name"] = dog.get_name()
        # temp fix until we can display images reliably
        dog_info["image_path"] = dog.get_thumb()
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
                "address" : dog_result.get_street_address,
                "city" : dog_result.get_city,
                "zipcode" : dog_result.get_zipcode,
                "owner_name" : dog_result.get_owner,
                "owner_email" : dog_result.get_email,
                "owner_phone" : dog_result.get_phone_number,
            })
            
            for match in matches:
                walker_query = match.get_walker
                walker_email = match.get_walker_email
                data["match_results"].append({
                    "dog" : match.get_dog,
                    "walker" : walker_query,
                    "walker_email" : walker_email,
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

def dog_list(request):
    # only able to view master list if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:
        # get all dogs in db
        dogs = Dog.objects.all()
        data = {'dogs':[]}
        # for each dog populate a dictionary w/ name, img, address, and db id
        for dog in dogs:
            data['dogs'].append({
                'name': dog.get_name,
                'owner_name' : dog.get_owner_name,
                'owner_phone': dog.get_phone_number,
                'owner_email': dog.get_email,
                'street_address': dog.get_street_address,
                'city': dog.get_city,
                'zipcode' : dog.get_zipcode,
                'id': dog.id,
                'image': dog.get_thumb(),
                'visible': dog.get_visible(),
            })
        data['dogs'].sort(key=visibility_key)
        return render(request, 'core/dog_list.html', data) 
    else:
        raise PermissionDenied()

def visibility_key(dog) :
    return not dog['visible']

def edit_dog(request):
    # only able to edit dogs if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:

        # get dog with id matchin=g url parameter
        dog_id = request.GET.get('q', '')

        # redirect back to list if id doesn't exist in db
        if not Dog.objects.filter(id=dog_id).exists():
            return redirect('dog_list')
        selected_dog = Dog.objects.get(id=dog_id)

        # POST request
        if request.method == 'POST':

            # save dog info if save button is pressed
            if 'save_dog' in request.POST:
                # assigning name, address from POST request
                selected_dog.dog_name = request.POST.get('dog_name')
                selected_dog.dog_info = request.POST.get('dog_info')
                selected_dog.owner_name = request.POST.get('owner_name')
                selected_dog.owner_phone = request.POST.get('owner_phone')
                selected_dog.owner_email = request.POST.get('owner_email')
                selected_dog.street_address = request.POST.get('street_address')
                selected_dog.city = request.POST.get('city')
                selected_dog.zipcode = request.POST.get('zipcode')
                selected_dog.visible = request.POST.get('dog_visible') == 'on'
                if not request.POST.get('image') == '':
                    selected_dog.image_path = request.POST.get('image')

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
            name = selected_dog.get_name
            info = selected_dog.get_info
            owner_name = selected_dog.get_owner_name
            phone_number = selected_dog.get_phone_number
            if phone_number == None:
                phone_number = ''
            email = selected_dog.get_email
            street_address = selected_dog.get_street_address
            city = selected_dog.get_city
            zipcode = selected_dog.get_zipcode
            image = selected_dog.get_thumb

            # two dictionaries passed to render:
            #   data: used by django framework to format walk times table
            #   json_data: used by js to display all stored walk times
            data = {
                'dog': {
                    'name': name,
                    'info': info,
                    'owner_name': owner_name,
                    'phone': phone_number,
                    'email': email,
                    'street_address': street_address,
                    'city': city,
                    'zipcode': zipcode,
                    'image': image,
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
            return render(request, 'core/edit_dog.html', {'data':data, 'json_data':dumps(json_data), 'image_form':S3DirectUploadForm()})
    else:
        # permission denied if user isn't staff
        raise PermissionDenied()

def add_dog(request):
    # only able to add dogs if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:

        # POST request
        if request.method == 'POST':

            if 'save_dog' in request.POST:
                # assigning name, address from POST request
                name_in = request.POST.get('dog_name')
                info_in = request.POST.get('dog_info')
                owner_name_in = request.POST.get('owner_name')
                owner_phone_in = request.POST.get('owner_phone')
                owner_email_in = request.POST.get('owner_email')
                street_address_in = request.POST.get('street_address')
                city_in = request.POST.get('city')
                zipcode_in = request.POST.get('zipcode')
                visible_in = request.POST.get('dog_visible') == 'on'
                image_in = request.POST.get('image')

                # assigning times from POST using checkbox id convention: "Thursday-2:00pm"
                chosen_times = []
                for day in DAYS:
                    for hour in HOURS:
                        chosen_times.append(request.POST.get(day + '-' + hour) == 'on')
                
                new_dog = Dog(
                    dog_name=name_in,
                    dog_info=info_in,
                    owner_name=owner_name_in,
                    owner_phone=owner_phone_in,
                    owner_email=owner_email_in,
                    street_address=street_address_in,
                    city=city_in,
                    zipcode=zipcode_in,
                    visible=visible_in,
                    times=chosen_times,
                    image_path=image_in,
                )

                new_dog.save()
            
            return redirect('dog_list')
        else:
            data = {
                'days': DAYS,
                'hours': HOURS,
                'image_form': S3DirectUploadForm(),
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

        # POST request
        if request.method == 'POST':

            # only save if save button was pressed
            if 'save_walker' in request.POST:

                # getting walker info from request
                walker.name = request.POST.get('walker_name')
                walker.phone_number = request.POST.get('walker_phone')

                walker.save()

            # redirect to home if cancel button is pressed
            elif 'cancel' in request.POST:
                return redirect('home')

        name = walker.get_name()
        email = walker.get_email()
        phone_number = walker.get_phone_number()
        if phone_number == None:
            phone_number = ''

        # display matches
        match_list = Match.objects.filter(walker__email=username)
        cleaned_matches = [{'dog_name': m.dog.dog_name,
                            "day":m.day, 
                            "start_time": m.get_start_time(),
                            "end_time": m.get_end_time(),} 
                        for m in match_list]

        matched_dogs = []
        for m in match_list:
            if m.dog not in matched_dogs:
                matched_dogs.append(m.dog)

        owner_info = [ {'dog_name': d.get_name(),
                        'owner_name': d.get_owner_name(), 
                        'owner_number': d.get_phone_number(),
                        'owner_email': d.get_email(),
                        'address': (d.get_street_address() + ", " + d.get_city() + ", " + d.get_zipcode()),
                        }  
                    for d in matched_dogs]

        my_dogs_other_walkers = []
        for dog in matched_dogs:
            dogs_matches = Match.objects.filter(dog=dog)
            dog_info = {'dog_name': dog.get_name()}
            dog_info_walker_list = []
            for dm in dogs_matches:
                if(dm.get_walker_email() != username and dm.walker not in dog_info_walker_list):
                    dog_info_walker_list.append(dm.walker)
            if (len(dog_info_walker_list) != 0):
                dog_info['other_walkers'] = dog_info_walker_list
                my_dogs_other_walkers.append(dog_info)

        data = {
            'walker': {
                'name': name,   
                'email': email,
                'phone': phone_number,
                'saved': ('save_walker' in request.POST),
            },
            'match_list': cleaned_matches,
            'owner_info': owner_info,
            'my_dogs_other_walkers': my_dogs_other_walkers,
        }

        return render(request, 'core/edit_walker.html', {'data':data})
    else:
        raise PermissionDenied()

def walker_signup(request):
    global form_is_open
    #print(form_is_open)
    
    # only able to edit walker profile if logged in as a normal user, not staff
    if request.user.is_authenticated and form_is_open:
        
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

        # POST request
        if request.method == 'POST':

            # getting walker info from request
            walker.name = request.POST.get('walker_name')
            walker.phone_number = request.POST.get('walker_phone')

            # iterate through checkboxes to fill out chosen_times
            chosen_times = []
            for day in DAYS:
                for hour in HOURS:
                    chosen_times.append(request.POST.get(day + '-' + hour) == 'on')
            walker.times = chosen_times

            # iterate through dog preferences to fill out dog_choices
            dog_choices = []
            for choice_num in range(PREF_COUNT):
                dropdown_choice = request.POST.get(f'dog_select_{choice_num + 1}')

                # append chosen dog name to dog_choices
                if Dog.objects.filter(dog_name=dropdown_choice).exists():
                    dog_choices.append(Dog.objects.get(dog_name=dropdown_choice).get_name())
                    
                # if '----' is chosen for a dog pref, then the pref is saved as None
                else:
                    dog_choices.append(None)
            
            walker.dog_choices = dog_choices
            walker.set_filledForm(True)
            walker.save()

            return redirect('home')

        name = walker.get_name()
        phone_number = walker.get_phone_number()
        if phone_number == None:
            phone_number = ''

        # getting dog names to display in pref dropdowns
        all_dogs = Dog.objects.all()
        visible_dogs = {}
        for dog in all_dogs:
            if dog.get_visible(): # only displaying dogs which have visible = True
                visible_dogs[dog.get_name()] = dog.get_walktimes()
        
        # helper array for Django template to loop through
        pref_nums = range(1, PREF_COUNT+1)

        data = {
            'walker': {
                'name': name,
                'phone': phone_number,
            },
            'days': DAYS,
            'hours': HOURS,
            'saved': (request.method == 'POST'),
            'pref_nums': pref_nums,
        }
        json_data = {
            'days': DAYS,
            'hours': HOURS,
            'times': walker.get_walktimes(),
            'prev_choices': walker.get_dog_choices(),
            'dog_list': visible_dogs,
            'pref_count': PREF_COUNT,
        }
        return render(request, 'core/walker_signup.html', {'data':data, 'json_data':dumps(json_data), 'form_is_open':form_is_open})
    elif not form_is_open:
        return render(request, 'core/walker_signup.html', {'form_is_open':form_is_open})
    else:
        raise PermissionDenied()

def admin_ctrl(request):
    # Booleans to check which button was pressed
    success = False
    clear = False
    clear_user_times = False
    global form_is_open

    # only able to edit dogs if logged in as staff
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'GET':
            return render(request, 'core/admin_ctrl.html')
        elif request.method == 'POST':
            if 'match' in request.POST:	
                all_dogs = Dog.objects.all()
                all_walkers = list(Walker.objects.all())

                random.shuffle(all_walkers)
                
                day_names = ['monday', 'tuesday', 
                            'wednesday', 'thursday', 'friday', 
                            'saturday','sunday']

                #   for each pref (1-5)
                #       for each walker
                #           check that walker hasn't already been matched with dif dog
                #               for each time
                #                   match walker with dog if both available
                #
                #   **only match walker with one dog per round
                #   **walkers randomized instead of signup order priority
                walker_matches = {}

                for walker in all_walkers:
                    len_prefs = len(walker.dog_choices)
                    for pref in range(len_prefs):

                        if not walker.get_name() in walker_matches:
                            walker_matches[walker.get_name()] = None

                        dog_name = walker.dog_choices[pref]

                        # check matches if pref isn't blank and walker isn't matched with other dogs
                        if (not dog_name == None and (walker_matches[walker.get_name()] == dog_name or walker_matches[walker.get_name()] == None)):
                            print("DOGNAME:")
                            print(dog_name)
                            dog = Dog.objects.get(dog_name=dog_name)
                            dog_walktimes = dog.get_walktimes()
                            walker_walktimes = walker.get_walktimes()

                            # for each day the dog needs to be walked
                            for i, day in enumerate(dog_walktimes):
                                # for each time the dog needs to be walked
                                for j, time in enumerate(day):
                                    # if both are free
                                    if (time and walker_walktimes[i][j] and not walker.check_walk(i, j) and not dog.check_walk(i, j)):
                                        # mark that walker is walking a dog and dog is being walked
                                        walker.set_walk(i,j)
                                        dog.set_walk(i,j)

                                        day_name = day_names[i]

                                        new_match = Match(
                                            dog=dog,
                                            walker=walker,
                                            day=day_name,
                                            time=j+9
                                        )
                                        new_match.save()
                                        
                                        walker.save()
                                        dog.save()

                                        if walker_matches[walker.get_name()] == None:
                                            walker_matches[walker.get_name()] = dog_name

                success = True

                return render(request, 'core/admin_ctrl.html', {'success':success})

            elif 'delete' in request.POST:				
                # get all matches, dogs, and walkers
                matches = Match.objects.all()
                dogs = Dog.objects.all()
                walkers = Walker.objects.all()

                # delete all matches
                for match in matches:
                    match.delete()
                
                # clear walking_times arrays for all dogs and walkers
                for dog in dogs:
                    dog.clear_matches()
                    dog.save()
                for walker in walkers:
                    walker.clear_matches()
                    walker.save()

                clear = True

                return render(request, 'core/admin_ctrl.html', {'clear':clear})
            elif 'clearUserTimes' in request.POST:
                walkers = Walker.objects.all()

                for walker in walkers:
                    walker.clear_user_times()
                    walker.save()
                
                clear_user_times = True

                return render(request, 'core/admin_ctrl.html', {'clear_user_times':clear_user_times})
            elif 'openForm' in request.POST:
                # reset walker filledForm booleans to False
                walkers = Walker.objects.all()

                for walker in walkers:
                    print(walker.get_name(), walker.get_filledForm())
                    walker.set_filledForm(False)
                    walker.save()
                    print(walker.get_name(), walker.get_filledForm())

                # set the form to open
                form_is_open = True

                return render(request, 'core/admin_ctrl.html')
                
            elif 'closeForm' in request.POST:
                walkers = Walker.objects.all()

                for walker in walkers:
                    print(walker.get_name(), walker.get_filledForm())
                
                form_is_open = False
                return render(request, 'core/admin_ctrl.html')
                
            else:
                clear = False
                success = False
                clear_user_times = False
                return render(request, 'core/admin_ctrl.html', {'success':success, 'clear':clear, 'clear_user_times':clear_user_times})
            
