from django.contrib import admin

# Register your models here.
from .models import Dog, Walker, Match, Form_Open_Tracker


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
    # display when viewling all dogs
    list_display = ('dog_name', 'owner_name')

    # fields when opening a single dogmodel
    fieldsets = [
        ('Dog Info', {'fields': ('dog_name', 'dog_info', 'image_path')}),

        ('Owner Info',
            {'fields': ('owner_name', 'owner_phone', 'owner_email',
                        'street_address', 'city', 'zipcode')}),
    ]
  
admin.site.register(Dog, DogAdmin)

class WalkerAdmin(admin.ModelAdmin):
    # #display when viewling all dogs
    list_display = ('name', 'email', 'phone_number')

    #fields when opening a single dogmodel
    fieldsets = [
        ('Walker Info', {'fields': ('name', 'email', 'phone_number', 
            'dog_choices', 'times')})
    ]

admin.site.register(Walker, WalkerAdmin)

admin.site.register(Match, Form_Open_Tracker)