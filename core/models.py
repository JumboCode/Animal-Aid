from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Dog(models.Model):
    # location = models.CharField(max_length=100)
    # zip_code = models.IntegerField() 
    # image = models.ImageField(height_field=350, max_length=100, upload_to='static/img/dogs/')

    # Updated Fields
    dog_name = models.CharField(max_length=30)
    dog_info = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=50)
    # owner_email
    # owner_phone
    address = models.CharField(max_length=100)
    # image = models.ImageField()
    # need to install pillow for image field
    
    sunday_nine_am   = models.BooleanField()
    sunday_ten_am    = models.BooleanField()
    sunday_eleven_am = models.BooleanField()
    sunday_noon      = models.BooleanField()
    sunday_one_pm    = models.BooleanField()
    sunday_two_pm    = models.BooleanField()
    sunday_three_pm  = models.BooleanField()
    sunday_four_pm   = models.BooleanField()
    sunday_five_pm   = models.BooleanField()

    monday_nine_am   = models.BooleanField()
    monday_ten_am    = models.BooleanField()
    monday_eleven_am = models.BooleanField()
    monday_noon      = models.BooleanField()
    monday_one_pm    = models.BooleanField()
    monday_two_pm    = models.BooleanField()
    monday_three_pm  = models.BooleanField()
    monday_four_pm   = models.BooleanField()
    monday_five_pm   = models.BooleanField()

    tuesday_nine_am   = models.BooleanField()
    tuesday_ten_am    = models.BooleanField()
    tuesday_eleven_am = models.BooleanField()
    tuesday_noon      = models.BooleanField()
    tuesday_one_pm    = models.BooleanField()
    tuesday_two_pm    = models.BooleanField()
    tuesday_three_pm  = models.BooleanField()
    tuesday_four_pm   = models.BooleanField()
    tuesday_five_pm   = models.BooleanField()

    wednesday_nine_am   = models.BooleanField()
    wednesday_ten_am    = models.BooleanField()
    wednesday_eleven_am = models.BooleanField()
    wednesday_noon      = models.BooleanField()
    wednesday_one_pm    = models.BooleanField()
    wednesday_two_pm    = models.BooleanField()
    wednesday_three_pm  = models.BooleanField()
    wednesday_four_pm   = models.BooleanField()
    wednesday_five_pm   = models.BooleanField()

    thursday_nine_am   = models.BooleanField()
    thursday_ten_am    = models.BooleanField()
    thursday_eleven_am = models.BooleanField()
    thursday_noon      = models.BooleanField()
    thursday_one_pm    = models.BooleanField()
    thursday_two_pm    = models.BooleanField()
    thursday_three_pm  = models.BooleanField()
    thursday_four_pm   = models.BooleanField()
    thursday_five_pm   = models.BooleanField()

    friday_nine_am   = models.BooleanField()
    friday_ten_am    = models.BooleanField()
    friday_eleven_am = models.BooleanField()
    friday_noon      = models.BooleanField()
    friday_one_pm    = models.BooleanField()
    friday_two_pm    = models.BooleanField()
    friday_three_pm  = models.BooleanField()
    friday_four_pm   = models.BooleanField()
    friday_five_pm   = models.BooleanField()

    saturday_nine_am   = models.BooleanField()
    saturday_ten_am    = models.BooleanField()
    saturday_eleven_am = models.BooleanField()
    saturday_noon      = models.BooleanField()
    saturday_one_pm    = models.BooleanField()
    saturday_two_pm    = models.BooleanField()
    saturday_three_pm  = models.BooleanField()
    saturday_four_pm   = models.BooleanField()
    saturday_five_pm   = models.BooleanField()

    class Meta:
        ordering = ['dog_name']

    # Clean data.
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

    # def get_location(self):
    #     return self.address
    
    # def get_image(self):
    #     return self.image
    
    # def get_walktimes(self):
    #     return {
    #         9  : self.nine_am,
    #         10 : self.ten_am,
    #         11 : self.eleven_am,
    #         12 : self.noon,
    #         13 : self.one_pm,
    #         14 : self.two_pm,
    #         15 : self.three_pm,
    #         16 : self.four_pm,
    #         17 : self.five_pm,
    #     }
    
    def __str__(self):
        return self.dog_name


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

class Walker(models.Model):
    class Meta:
        ordering = ['name']
        
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    
    dog_1 = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog1")
    dog_2 = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog2")
    dog_3 = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog3")
    dog_4 = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog4")
    dog_5 = models.ForeignKey(Dog, on_delete=models.SET_NULL, blank=True, null=True, related_name="dog5")
    
    sunday_nine_am   = models.BooleanField()
    sunday_ten_am    = models.BooleanField()
    sunday_eleven_am = models.BooleanField()
    sunday_noon      = models.BooleanField()
    sunday_one_pm    = models.BooleanField()
    sunday_two_pm    = models.BooleanField()
    sunday_three_pm  = models.BooleanField()
    sunday_four_pm   = models.BooleanField()
    sunday_five_pm   = models.BooleanField()

    monday_nine_am   = models.BooleanField()
    monday_ten_am    = models.BooleanField()
    monday_eleven_am = models.BooleanField()
    monday_noon      = models.BooleanField()
    monday_one_pm    = models.BooleanField()
    monday_two_pm    = models.BooleanField()
    monday_three_pm  = models.BooleanField()
    monday_four_pm   = models.BooleanField()
    monday_five_pm   = models.BooleanField()

    tuesday_nine_am   = models.BooleanField()
    tuesday_ten_am    = models.BooleanField()
    tuesday_eleven_am = models.BooleanField()
    tuesday_noon      = models.BooleanField()
    tuesday_one_pm    = models.BooleanField()
    tuesday_two_pm    = models.BooleanField()
    tuesday_three_pm  = models.BooleanField()
    tuesday_four_pm   = models.BooleanField()
    tuesday_five_pm   = models.BooleanField()

    wednesday_nine_am   = models.BooleanField()
    wednesday_ten_am    = models.BooleanField()
    wednesday_eleven_am = models.BooleanField()
    wednesday_noon      = models.BooleanField()
    wednesday_one_pm    = models.BooleanField()
    wednesday_two_pm    = models.BooleanField()
    wednesday_three_pm  = models.BooleanField()
    wednesday_four_pm   = models.BooleanField()
    wednesday_five_pm   = models.BooleanField()

    thursday_nine_am   = models.BooleanField()
    thursday_ten_am    = models.BooleanField()
    thursday_eleven_am = models.BooleanField()
    thursday_noon      = models.BooleanField()
    thursday_one_pm    = models.BooleanField()
    thursday_two_pm    = models.BooleanField()
    thursday_three_pm  = models.BooleanField()
    thursday_four_pm   = models.BooleanField()
    thursday_five_pm   = models.BooleanField()

    friday_nine_am   = models.BooleanField()
    friday_ten_am    = models.BooleanField()
    friday_eleven_am = models.BooleanField()
    friday_noon      = models.BooleanField()
    friday_one_pm    = models.BooleanField()
    friday_two_pm    = models.BooleanField()
    friday_three_pm  = models.BooleanField()
    friday_four_pm   = models.BooleanField()
    friday_five_pm   = models.BooleanField()

    saturday_nine_am   = models.BooleanField()
    saturday_ten_am    = models.BooleanField()
    saturday_eleven_am = models.BooleanField()
    saturday_noon      = models.BooleanField()
    saturday_one_pm    = models.BooleanField()
    saturday_two_pm    = models.BooleanField()
    saturday_three_pm  = models.BooleanField()
    saturday_four_pm   = models.BooleanField()
    saturday_five_pm   = models.BooleanField()

    # dog_1_nine_am   = models.BooleanField()
    # dog_1_ten_am    = models.BooleanField()
    # dog_1_eleven_am = models.BooleanField()
    # dog_1_noon      = models.BooleanField()
    # dog_1_one_pm    = models.BooleanField()
    # dog_1_two_pm    = models.BooleanField()
    # dog_1_three_pm  = models.BooleanField()
    # dog_1_four_pm   = models.BooleanField()
    # dog_1_five_pm   = models.BooleanField()
    
    # dog_2_nine_am   = models.BooleanField()
    # dog_2_ten_am    = models.BooleanField()
    # dog_2_eleven_am = models.BooleanField()
    # dog_2_noon      = models.BooleanField()
    # dog_2_one_pm    = models.BooleanField()
    # dog_2_two_pm    = models.BooleanField()
    # dog_2_three_pm  = models.BooleanField()
    # dog_2_four_pm   = models.BooleanField()
    # dog_2_five_pm   = models.BooleanField()
    
    # dog_3_nine_am   = models.BooleanField()
    # dog_3_ten_am    = models.BooleanField()
    # dog_3_eleven_am = models.BooleanField()
    # dog_3_noon      = models.BooleanField()
    # dog_3_one_pm    = models.BooleanField()
    # dog_3_two_pm    = models.BooleanField()
    # dog_3_three_pm  = models.BooleanField()
    # dog_3_four_pm   = models.BooleanField()
    # dog_3_five_pm   = models.BooleanField()
    
    # dog_4_nine_am   = models.BooleanField()
    # dog_4_ten_am    = models.BooleanField()
    # dog_4_eleven_am = models.BooleanField()
    # dog_4_noon      = models.BooleanField()
    # dog_4_one_pm    = models.BooleanField()
    # dog_4_two_pm    = models.BooleanField()
    # dog_4_three_pm  = models.BooleanField()
    # dog_4_four_pm   = models.BooleanField()
    # dog_4_five_pm   = models.BooleanField()
    
    # dog_5_nine_am   = models.BooleanField()
    # dog_5_ten_am    = models.BooleanField()
    # dog_5_eleven_am = models.BooleanField()
    # dog_5_noon      = models.BooleanField()
    # dog_5_one_pm    = models.BooleanField()
    # dog_5_two_pm    = models.BooleanField()
    # dog_5_three_pm  = models.BooleanField()
    # dog_5_four_pm   = models.BooleanField()
    # dog_5_five_pm   = models.BooleanField()
   
    def __str__(self):
        return self.name
