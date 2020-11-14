from django.db import models

class Form(models.Model):
	form_name = models.CharField(max_length=100)
	pubdate = models.DateTimeField('date pubbed')

	def __str__(self):
		return self.form_name


class Field(models.Model):
	forms = models.ForeignKey(Form, on_delete=models.CASCADE, default=1)
	# textField = models.CharField(max_length=200)
	# votes = models.IntegerField(default=0)

	# forms = models.ForeignKey(Form, on_delete=models.CASCADE)
	textField = models.CharField(max_length=200)
	testBool = models.BooleanField('test bool', default=1)