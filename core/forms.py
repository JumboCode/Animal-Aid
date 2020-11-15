from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.password_validation import *


SpecialSym =['$', '@', '#', '%', '*', '!', '^', '&', '(', ')', '?']

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


################ DYNAMIC SIGNUP VALIDATION FUNCS #######################

# make sure the email ends with tufts.edu
# we may want to make sure it is unique later (but not doing that dynamically)
def validate_username(request):
    email = str(request.GET.get('email',None))
    data = {
        'tufts_edu': email.endswith("@tufts.edu"),
    }
    return JsonResponse(data)

# check if the password meets the 4 following criteria:
    # over 6 characters long
    # contains a special character (not weak)
    # not a common tester password that is easy to hack
    # is not only numeric
def check_password(passwd):
    data = {
        'too_short': len(passwd) < 6,
        'no_special_char': not any(char in SpecialSym for char in passwd),
        'too_common': passwd == "test" or passwd == "testtest" or "123" in passwd or "abc" in passwd,
        'only_digits': passwd.isdigit()
    }
    return data

# helper function to ensure that the password meets all 4 criteria
def synthesize(data):
    return True if all([not value for value in data.values()]) else False

# validate first password field dynamically
def validate_password1(request):
    password1 = str(request.GET.get('password1',None))
    data = check_password(password1)
    return JsonResponse(data)

# validate second password field dynamically
# this time, also check to ensure that the two passwords match
def validate_password2(request):
    password1 = str(request.GET.get('password1',None))
    password2 = str(request.GET.get('password2',None))
    pwd1_data = check_password(password1)
    data = dict()
    data['strong_pass'] = synthesize(pwd1_data)
    data['is_matching'] = password1 == password2
    return JsonResponse(data)

class LoginForm(AuthenticationForm):
    # Fields default to username and password from parent class.

    class Meta:
        model = User
        fields = ["username", "password"]
    
    def confirm_login_allowed(self, user):
        pass



# ################ FORM BUILDER #######################
# class FormBuilderForm(forms.ModelForm):








