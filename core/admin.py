from django.contrib import admin

# Register your models here.
from .models import Dog, Walker

class Dogs(admin.ModelAdmin):
    list_display= ('name', 'location', 'zip_code')


class DogModelForm(forms.modelForm):
	#additional fields
	info = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    #MISSING: WALK TIMES


	class Meta:
		model = Dog
		fields = '__all__'

class DogModelAdmin(admin.ModelAdmin)
	form = DogModelForm

	fieldsets = (
		(None, {
			'fields': ('dog_name', 'info', 'owner_name', 'address', 'image', 'walk_times')
			}),
		)
  
admin.site.register(Dog, Dogs)

admin.site.register(Walker)
