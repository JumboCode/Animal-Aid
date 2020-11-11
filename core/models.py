from django.db import models

# Create your models here.
class DogModel(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    
    # TODO: Specify a path for uploaded pictures.
    image = models.ImageField(upload_to=None)

    morning_walk = models.BooleanField()
    midday_walk  = models.BooleanField()
    evening_walk = models.BooleanField()
    night_walk   = models.BooleanField()

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
            "morning": self.morning_walk,
            "midday" : self.midday_walk,
            "evening": self.evening_walk,
            "night"  : self.night_walk
        }
    
    
