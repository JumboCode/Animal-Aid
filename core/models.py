from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    zip_code = models.IntegerField() 
    image = models.ImageField(upload_to='static/img/dogs/')

    nine_am   = models.BooleanField()
    ten_am    = models.BooleanField()
    eleven_am = models.BooleanField()
    noon      = models.BooleanField()
    one_pm    = models.BooleanField()
    two_pm    = models.BooleanField()
    three_pm  = models.BooleanField()
    four_pm   = models.BooleanField()
    five_pm   = models.BooleanField()

    class Meta:
        ordering = ['name']

    # Clean data.
    def clean(self):
        if not (self.nine_am or self.ten_am or self.eleven_am or self.noon or
                self.one_pm or self.two_pm or self.three_pm or self.four_pm or
                self.five_pm):
            raise ValidationError("You must specify at least one walk time.")

    def walkable(self):
        return self.morning_walk or self.midday_walk or self.evening_walk or self.night_walk
    
    def get_name(self):
        return self.name

    def get_location(self):
        return self.location
    
    def get_image(self):
        return self.image
    
    def get_walktimes(self):
        return {
            9  : self.nine_am,
            10 : self.ten_am,
            11 : self.eleven_am,
            12 : self.noon,
            13 : self.one_pm,
            14 : self.two_pm,
            15 : self.three_pm,
            16 : self.four_pm,
            17 : self.five_pm,
        }
    
    def __str__(self):
        return self.name


class Match(models.Model):
    dog    = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog")
    
    # Walker model is not in here yet
    # walker = models.ForeignKey(Walker, on_delete=models.SET_NULL, blank=True, null=True, related_name="walker")
    day    = models.CharField(max_length=10)
    time   = models.PositiveIntegerField()

    def get_dog(self):
        return self.dog

    # def get_walker(self):
    #     return self.walker
    
    def get_day(self):
        return self.day 

    def get_time(self):
        return self.time

    def __str__(self):
        return self.dog.get_name() + " walked by " # + self.walker.get_name()