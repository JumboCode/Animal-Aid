from aws.conf import *
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from s3direct.fields import S3DirectField
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator

# constants to control how many walking times are used
DAYS = 7
HOURS = 9
STOCK_URL = 'https://st.depositphotos.com/1798678/3986/v/600/depositphotos_39864187-stock-illustration-dog-silhouette-vector.jpg'

# regex validator for phone number
phone_validator = RegexValidator(r'^(\+\d{1,2}\s)?\d{3}-\d{3}-\d{4}$', "Please enter a valid phone number (country code optional): +X XXX-XXX-XXXX")

# regex validator for zipcode
zip_validator = RegexValidator(r'^[0-9]{5}$', "Please enter a valid five digit zip code.")

class Dog(models.Model):
	# Updated Fields
	dog_name = models.CharField(max_length=30, null=True)
	dog_info = models.CharField(max_length=200, null=True)
	image_path = S3DirectField(dest='example_destination', blank=True)

	owner_name = models.CharField(max_length=50, null=True)
	owner_phone = models.CharField(max_length=100, null=True, validators=[phone_validator])
	owner_email = models.EmailField(max_length=100, null=True)
	street_address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	zipcode = models.CharField(max_length=5, null=True, validators=[zip_validator])

	visible = models.BooleanField(default=True)


	# Array of walk times as booleans
	def blank_times():
		times = []
		for day in range(DAYS * HOURS):
			times.append(False)
		return times

	# times dog needs to be walked
	times = ArrayField(
		models.BooleanField(),
		size=DAYS*HOURS,
		default=blank_times,
	)

	# times dog is being walked
	walking_times = ArrayField(
		models.BooleanField(),
		size=DAYS*HOURS,
		default=blank_times,
	)

	class Meta:
		ordering = ['dog_name']

	# TODO: Check all times of all days
	# def clean(self):
	#     if not (self.nine_am or self.ten_am or self.eleven_am or self.noon or
	#             self.one_pm or self.two_pm or self.three_pm or self.four_pm or
	#             self.five_pm):
	#         raise ValidationError("You must specify at least one walk time.")

	# def walkable(self):
	#     return self.morning_walk or self.midday_walk or self.evening_walk or self.night_walk
	
	def get_name(self):
		return self.dog_name

	def get_info(self):
		return self.dog_info

	def get_owner_name(self):
		return self.owner_name

	def get_street_address(self):
		return self.street_address
		
	def get_city(self):
		return self.city

	def get_zipcode(self):
		return self.zipcode


	def get_phone_number(self):
		return self.owner_phone
		
	def get_email(self):
		return self.owner_email
		
	def get_owner(self):
		return self.owner_name
	
	def get_image(self):
		if self.image_path == '' or self.image_path == None:
			return STOCK_URL
		return self.image_path

	def get_visible(self):
		return self.visible
	
	# takes 2D ArrayField times and maps to 3D array for use in front-end
	def get_walktimes(self):
		out_times = []
		for day in range(DAYS):
			out_times.append(self.times[day * HOURS : day * HOURS + HOURS])
		return out_times

	def set_walk(self, day, time):
		self.walking_times[HOURS * day + time] = True
	
	# check if dog is currently being walked at that time
	def check_walk(self, day, time):
		return self.walking_times[HOURS * day + time]
	
	def __str__(self):
		return self.dog_name


class Walker(models.Model):
	class Meta:
		ordering = ['name']
		
	name = models.CharField(max_length=30)
	email = models.EmailField(max_length=100, null=True)
	phone_number = models.CharField(max_length=100, null=True, validators=[phone_validator])
	
	def blank_choices():
		return []

	dog_choices = ArrayField(
		models.CharField(max_length=16),
		default=blank_choices,
	)

	# Array of walk times as booleans
	def blank_times():
		times = []
		for day in range(DAYS * HOURS):
			times.append(False)
		return times

	# times walker is free
	times = ArrayField(
		models.BooleanField(),
		size=DAYS*HOURS,
		default=blank_times,
	)

	# times walker is walking a dog
	walking_times = ArrayField(
		models.BooleanField(),
		size=DAYS*HOURS,
		default=blank_times,
	)

	def get_name(self):
		return self.name
	
	def get_email(self):
		return self.email

	def get_email(self):
		return self.email

	def get_phone_number(self):
		return self.phone_number

	def get_dog_choices(self):
		return self.dog_choices

	# takes 2D ArrayField times and maps to 3D array for use in front-end
	def get_walktimes(self):
		out_times = []
		for day in range(DAYS):
			out_times.append(self.times[day * HOURS : day * HOURS + HOURS])
		return out_times
   
	def set_walk(self, day, time):
		self.walking_times[HOURS * day + time] = True
	
	# check if walker is walking a dog at that time
	def check_walk(self, day, time):
		return self.walking_times[HOURS * day + time]
		
	def __str__(self):
		return self.name


class Match(models.Model):
	# ID, dog, day, time, walker
	dog    = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog")
	walker = models.ForeignKey(Walker, on_delete=models.SET_NULL, blank=True, null=True, related_name="walker")
	day    = models.CharField(max_length=10)
	time   = models.PositiveIntegerField()

	def get_dog(self):
		return self.dog

	def get_walker(self):
		return self.walker.get_name()
	
	def get_walker_email(self):
		return self.walker.get_email()
	
	def get_day(self):
		return self.day 

	def get_start_time(self):
		return self.time

	def get_end_time(self):
		return self.time + 1

	def __str__(self):
		print_str = str(self.dog) + " (dog) walked by " + str(self.walker) + " (walker) on "
		print_str += str(self.day) + "s at " + str(self.time) + " o'clock"
		return print_str
