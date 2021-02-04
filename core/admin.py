from django.contrib import admin

# Register your models here.
from .models import Dog, Walker

class Dogs(admin.ModelAdmin):
    list_display= ('name', 'location', 'zip_code')


class DogModelForm(forms.modelForm):
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
