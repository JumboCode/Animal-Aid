from django.db import models
from django.core.validators import MinValueValidator

# class FormDisplay(models.Model):
# 	displayed_form_id = models.IntegerField('displayed form id', default=1)

# 	def return_id(self):
# 		return displayed_form_id


class Form(models.Model):
	# # make Form a child of FormDisplay
	# form_display = models.ForeignKey(FormDisplay, on_delete=models.CASCADE, default=1)

	form_name = models.CharField(max_length=100)
	pubdate = models.DateTimeField('date published')

	#true if this form is intended for walker model
	walker_bool = models.BooleanField('form for walker info', default=1)

	#true if this form should be displayed
	display_form = models.BooleanField('If form should be displayed', default=0)

	def __str__(self):
		return self.form_name

	def form_id(self):
		return self.id


class Field(models.Model):
	#make Field a child of Form
	forms = models.ForeignKey(Form, related_name='field', on_delete=models.CASCADE, default=1)

	#setting up label name
	label = models.CharField(max_length=200, blank=True)

	#determining which field type
	#defining constants
	TEXT_FIELD = 'TF'
	CHECKLIST = 'CL'
	NUMBER = 'NM'
	DROPDOWN = "DD"

	FIELD_TYPES = [
		('TF', 'Text Field'),
		('CL', 'Checklist'),
		('NM', 'Number'),
		('DD', 'Dropdown Menu'),
	]

	formType = models.CharField(max_length=20, choices=FIELD_TYPES, default='')

	options = models.CharField(max_length=200, blank=True)

	#required and visible bools
	requiredBool = models.BooleanField('field required', default=1)
	visibleBool = models.BooleanField('field visible', default=1)

	#ordering - validator to make sure it stays positive (applies only when made into ModelForm)
	order = models.IntegerField('field order', null=True, blank=True, validators=[MinValueValidator(0)], default=1)


# model to hold results for generic purposes
# class Result(models.Model):
# 	#which form's data we're storing
# 	form_id = models.PositiveIntegerField('form id')
# 	form_name = models.CharField(max_length=100)

