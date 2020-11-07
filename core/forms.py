from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Enter Tufts email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        if not email.endswith("@tufts.edu"):
            raise ValidationError("Invalid Tufts email address")
        return email

    def clean_password2(self):
        return super().clean_password2()

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user

class LoginForm(AuthenticationForm): # inherit from Authentication Form
    # Fields default to username and password from parent class.

    class Meta:
        model = User
        fields = ["username", "password"]
    
    def confirm_login_allowed(self, user):
        pass
