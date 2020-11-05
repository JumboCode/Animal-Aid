from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.password_validation import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Enter Tufts email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        print("CLEAN EMAIL WAS CALLED")
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(username=email)
        if r.exists():
            raise  ValidationError("A user with that email already exists")
        if not email.endswith("@tufts.edu"):
            raise ValidationError("Invalid Tufts email address")
        return email

    def clean_password2(self):
        print("CHECKING PASSWORD VALIDITY")
        return super().clean_password2()

    def save(self, commit=True):
        print("SAVING USER TO DB")
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
        )
        return user

def validate_username(request):
    email = str(request.GET.get('email',None))
    data = {
        'tufts_edu': email.endswith("@tufts.edu"),
    }
    if (data['tufts_edu'] == True):
        print("yay")
    return JsonResponse(data)

def validate_password1(request):
    SpecialSym =['$', '@', '#', '%', '*']
    password1 = str(request.GET.get('password1',None))
    data = {
        'too_short': len(password1) < 6,
        'no_special_char': not any(char in SpecialSym for char in password1),
        'too_common': password1 == "test" or password1 == "testtest" or "123" in password1 or "abc" in password1,
        'only_digits': password1.isdigit()
    }
    return JsonResponse(data)

class LoginForm(AuthenticationForm):
    # Fields default to username and password from parent class.

    class Meta:
        model = User
        fields = ["username", "password"]
    
    def confirm_login_allowed(self, user):
        pass