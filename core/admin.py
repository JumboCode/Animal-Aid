from django.contrib import admin

# Register your models here.
from .models import Dog, Walker

class Dogs(admin.ModelAdmin):
    list_display= ('name', 'location', 'zip_code')
  
admin.site.register(Dog, Dogs)

admin.site.register(Walker)
