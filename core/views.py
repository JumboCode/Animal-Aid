from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
import django.contrib.auth.forms as forms

def home(request):
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.as_p())
        if form.is_valid():
            try:
                form.save()
                username = form.cleaned_data.get('username')
                if not username.endswith('@tufts.edu'):
                    form.add_error("username", "Please enter a valid Tufts email address")
                    raise forms.ValidationError("Please enter a valid Tufts email address")
            except:
                return render(request, 'core/signup.html', {'form': form})
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
    
def error(request):
    return render(request, 'core/error.html')