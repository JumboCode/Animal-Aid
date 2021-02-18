from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# constants to control how many walking times are used
DAYS = 7
HOURS = 9

class Dog(models.Model):
    # Updated Fields
    dog_name = models.CharField(max_length=30)
    dog_info = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    visible = models.BooleanField(default=True)

    #location = models.CharField(max_length=100)
    #zip_code = models.IntegerField() 
    #image = models.ImageField(upload_to='static/img/dogs/', null=True)

    # Array of walk times as booleans
    
    def blank_times():
        times = []
        for day in range(DAYS * HOURS):
            times.append(False)
        return times

    times = ArrayField(
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

    def get_address(self):
        return self.address
        
    # def get_zip(self):
    #     return self.zip_code
    
    # def get_image(self):
    #     return self.image

    def get_visible(self):
        return self.visible
    
    # takes 2D ArrayField times and maps to 3D array for use in front-end
    def get_walktimes(self):
        out_times = []
        for day in range(DAYS):
            out_times.append(self.times[day * HOURS : day * HOURS + HOURS])
        return out_times
    
    def __str__(self):
        return self.dog_name


class Walker(models.Model):
    class Meta:
        ordering = ['name']
        
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    
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

    times = ArrayField(
        models.BooleanField(),
        size=DAYS*HOURS,
        default=blank_times,
    )

    def get_name(self):
        return self.name

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
        return self.walker
    
    def get_day(self):
        return self.day 

    def get_time(self):
        return self.time

    def __str__(self):
        return self.dog.get_name() + " walked by " # + self.walker.get_name()# return "MATCH"
        print_str = str(self.dog) + " (dog) walked by " + str(self.walker) + " (walker) on "
        print_str += str(self.day) + "s at " + str(self.time) + " o'clock"
        return print_str
