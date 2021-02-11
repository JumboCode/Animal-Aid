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

        ('Sunday Walk Times', {
            'classes': ('collapse',),
            'fields': ('sunday_nine_am', 
                       'sunday_ten_am',  
                       'sunday_eleven_am',
                       'sunday_noon',    
                       'sunday_one_pm', 
                       'sunday_two_pm',  
                       'sunday_three_pm',
                       'sunday_four_pm',
                       'sunday_five_pm',)
            }),

        ('Monday Walk Times', {
            'classes': ('collapse',),
            'fields': ('monday_nine_am', 
                       'monday_ten_am',  
                       'monday_eleven_am',
                       'monday_noon',    
                       'monday_one_pm', 
                       'monday_two_pm',  
                       'monday_three_pm',
                       'monday_four_pm',
                       'monday_five_pm',)
            }),

        ('Tuesday Walk Times', {
            'classes': ('collapse',),
            'fields': ('tuesday_nine_am', 
                       'tuesday_ten_am',  
                       'tuesday_eleven_am',
                       'tuesday_noon',    
                       'tuesday_one_pm', 
                       'tuesday_two_pm',  
                       'tuesday_three_pm',
                       'tuesday_four_pm',
                       'tuesday_five_pm',)
            }),

        ('Wednesday Walk Times', {
            'classes': ('collapse',),
            'fields': ('wednesday_nine_am', 
                       'wednesday_ten_am',  
                       'wednesday_eleven_am',
                       'wednesday_noon',    
                       'wednesday_one_pm', 
                       'wednesday_two_pm',  
                       'wednesday_three_pm',
                       'wednesday_four_pm',
                       'wednesday_five_pm',)
            }),

        ('Thursday Walk Times', {
            'classes': ('collapse',),
            'fields': ('thursday_nine_am', 
                       'thursday_ten_am',  
                       'thursday_eleven_am',
                       'thursday_noon',    
                       'thursday_one_pm', 
                       'thursday_two_pm',  
                       'thursday_three_pm',
                       'thursday_four_pm',
                       'thursday_five_pm',)
            }),

        ('Friday Walk Times', {
            'classes': ('collapse',),
            'fields': ('friday_nine_am', 
                       'friday_ten_am',  
                       'friday_eleven_am',
                       'friday_noon',    
                       'friday_one_pm', 
                       'friday_two_pm',  
                       'friday_three_pm',
                       'friday_four_pm',
                       'friday_five_pm',)
            }),

        ('Saturday Walk Times', {
            'classes': ('collapse',),
            'fields': ('saturday_nine_am', 
                       'saturday_ten_am',  
                       'saturday_eleven_am',
                       'saturday_noon',    
                       'saturday_one_pm', 
                       'saturday_two_pm',  
                       'saturday_three_pm',
                       'saturday_four_pm',
                       'saturday_five_pm',)
            }),
    ]
  
admin.site.register(Dog, DogAdmin)

admin.site.register(Walker)

admin.site.register(Match)