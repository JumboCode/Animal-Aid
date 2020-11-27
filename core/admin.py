from django.contrib import admin

# Register your models here.
from .models import Dog, Walker

admin.site.register(Dog)
admin.site.register(Walker)
