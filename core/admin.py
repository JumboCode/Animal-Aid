from django.contrib import admin

# Register your models here.
from .models import DogModel

admin.site.register(DogModel)