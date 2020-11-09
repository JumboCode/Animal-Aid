from django.db import models

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    
    # TODO: Specify a path for uploaded pictures.
    image = models.ImageField(upload_to=None)

    morning_walk = models.BooleanField()
    midday_walk  = models.BooleanField()
    evening_walk = models.BooleanField()
    night_walk   = models.BooleanField()

    # TODO: maybe replace values with resp. variables?
    walktimes = {
        "morning" : False,
        "midday"  : False,
        "evening" : False,
        "night"   : False,
    }

    def walkable(self):
        return self.morning_walk or self.midday_walk or self.evening_walk or self.night_walk
    
    def get_name(self):
        return self.name

    def get_location(self):
        return self.location
    
    def get_image(self):
        return self.image
    
    def get_walktimes(self):
        return walktimes
    
    def update_walktimes(self, new_times):
        return None

    
