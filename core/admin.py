from django.contrib import admin

# Register your models here.
from .models import Dog, Walker, Match


# class DogModelForm(forms.modelForm):
#   #additional fields
#   info = models.CharField(max_length=200)
#     owner_name = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)
#     #MISSING: WALK TIMES


#   class Meta:
#       model = Dog
#       fields = '__all__'


class DogAdmin(admin.ModelAdmin):
    # #display when viewling all dogs
    list_display = ('dog_name', 'owner_name')

    #fields when opening a single dogmodel
    fieldsets = [
        ('Dog Info', {'fields': ('dog_name', 'dog_info')}),

        ('Owner Info', {'fields': ('owner_name', 'address')}),

    ]
  
admin.site.register(Dog, DogAdmin)

admin.site.register(Walker)

admin.site.register(Match)