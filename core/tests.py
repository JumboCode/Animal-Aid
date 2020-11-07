from django.test import TestCase
from django import forms
from .forms import CustomUserCreationForm, LoginForm
# import .views

from django.http import QueryDict
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO
from django.contrib.auth.models import AnonymousUser

# Create your tests here.

# Correct user and pass
# Correct user wrong pass
# Incorrect user


def GetFakeRequest(path, user):
  """ Construct a fake request(WSGIRequest) object"""
  req = WSGIRequest({
          'REQUEST_METHOD': 'POST',
          'PATH_INFO': path,
          'wsgi.input': StringIO()})

  return req

# https://gist.github.com/majgis/4164503
request = GetFakeRequest('/login/', 'test')

# https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.QueryDict
query_dict = QueryDict('csrfmiddlewaretoken=TOKEN&username=test&password=pass')

class LoginTestCase(TestCase):
    def test_login(self):
        # form_data = {'username': 'test', 'password': 'pass'}
        form = LoginForm(request, data=query_dict)
        print("------FORM------\n")
        print(form)
        print("------REQUEST------\n")
        print(request)
        print("------REQUEST.POST------\n")
        print(query_dict)
        self.assertTrue(form.is_valid())


        """
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
    # GET request
    form = LoginForm()
    return render(request, 'core/login.html', {'form': form})
    """