from django.contrib import admin, messages
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
	list_display = ('form_name', 'pubdate', 'form_id', 'display_form')

	#admin actions
	def make_displayed(self, request, queryset):
		if len(queryset) > 1:
			messages.error(request, 'Only 1 Form can be displayed!')
		else:
			queryset.update(display_form=True)
			# queryset[0].form_display.displayed_form_id = queryset[0].id
	make_displayed.short_description = "Display Selected Form (only 1)"

	def make_not_displayed(self, request, queryset):
		queryset.update(display_form=False)
	make_not_displayed.short_description = "Do not display Form(s)"

	actions = [make_displayed, make_not_displayed]


admin.site.register(Form, FormAdmin)


