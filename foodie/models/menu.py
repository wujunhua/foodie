from django.db import models

#
#   ##############################  MENU  ######################################
#
class Menu(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    price = models.IntegerField()
    rating = models.FloatField(default=0.0) #might not need this field
    num_ratings = models.IntegerField(default=0) #might not need this field
    times_ordered = models.IntegerField(default=0)
    image_url = models.TextField(max_length=100, default="")

    def update_rating(self, rating):
        self.rating =  (self.rating * self.num_ratings + rating) / (self.num_ratings + 1)
        self.num_ratings += 1
