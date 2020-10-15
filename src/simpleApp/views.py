from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages
from authtools import views as authviews
from braces import views as bracesviews
from django.conf import settings
from django.shortcuts import render
from . import forms
from django.http import HttpResponse

count = 0

def test(request):
    global count
    # return HttpResponse("hello")
    if request.method == "GET":
        count += 1
        return render(request, 'test.html', {"output": count})