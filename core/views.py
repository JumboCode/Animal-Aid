from django import forms
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from core.models import Form

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
            data = {'matches':[
                {
                    'dog_name': 'Fluffy',
                    'walker': 'Tyler',
                    'times': [6, 7, 3, 0, 1, 4, 6],
                },
                {
                    'dog_name': 'Cuddles',
                    'walker': 'Ann Marie',
                    'times': [12, 12, 12, 1, 1, 2, 0],
                },
            ]}
            return render(request, 'core/results.html', data)
        else:
            # GET req to load page
            return render(request, 'core/results.html')
    else:
        raise PermissionDenied()

def form_builder_view(request):
    if request.method == 'POST':
        built_form = Form.objects.get(form_name=request.POST.get('form'))

        form_data = {
            'title': built_form.form_name,
            'fields': []
        }
        for field in built_form.field.all():
            form_data['fields'].append ({ 
                'id': field.id,
                'prompt': field.label,
                'type': field.formType,
                'options': field.options.split(','),
                'order': field.order,
            })
        form_data['fields'].sort(key=by_id)
        return render(request, 'core/form_builder.html', {'form': form_data})
    else:
        form_list = Form.objects.all()
        form_data = {
            'title': 'Choose Your Form:',
            'fields': [{
                'id': 'form',
                'prompt': 'Form',
                'type': 'DD',
                'options': [],
            }]
        }
        for form in form_list:
            form_data['fields'][0]['options'].append(form.form_name)
        return render(request, 'core/form_builder.html', {'form': form_data})

def by_id(field_entry):
    return field_entry['order']