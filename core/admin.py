from django.contrib import admin
from .models import Form, Field


class FieldInLine(admin.TabularInline):
	model = Field
	extra = 0


class FormAdmin(admin.ModelAdmin):
	fieldsets = [
	(None, {'fields': ['form_name']}),
	('Date Information', {'fields': ['pubdate']}),
	]

	inlines = [FieldInLine]

	#add list display
	list_display = ('form_name', 'pubdate', 'display_form', 'form_id')

# Other method - change the template
# class FormBuilderAdmin(admin.ModelAdmin):
# 	list_display = 


admin.site.register(Form, FormAdmin)


