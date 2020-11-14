from django.contrib import admin

from .models import Form, Field

class FieldInLine(admin.TabularInline):
	model = Field
	extra = 1

class FormAdmin(admin.ModelAdmin):
	fieldsets = [
	(None, {'fields': ['form_name']}),
	('Date Information', {'fields': ['pubdate']}),
	]

	inlines = [FieldInLine]

admin.site.register(Form, FormAdmin)
