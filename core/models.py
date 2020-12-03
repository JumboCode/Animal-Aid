from django.db import models
from django.core.validators import MinValueValidator

class Form(models.Model):
	form_name = models.CharField(max_length=100)
	pubdate = models.DateTimeField('date pubbed')

	def __str__(self):
		return self.form_name


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
	order = models.IntegerField('field order', null=True, blank=True, validators=[MinValueValidator(0)])


