from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse


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
<<<<<<< HEAD
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
=======
            self.cleaned_data['email'],
            self.cleaned_data['password1']
>>>>>>> fixed redundant email error
        )
        return user

def validate_username(request):
    email = str(request.GET.get('username',None))
    data = {
        'tufts_edu': not email.endswith("@tufts.edu"),
        'is_taken': User.objects.filter(username=email).exists()
    }
    return JsonResponse(data)

class LoginForm(AuthenticationForm):
    # Fields default to username and password from parent class.

    class Meta:
        model = User
        fields = ["username", "password"]
    
    def confirm_login_allowed(self, user):
        pass
