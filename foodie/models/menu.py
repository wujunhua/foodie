from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    rating = models.FloatField(default=None)
    num_ratings = models.IntegerField(default=0)

    def update_rating(self, rating):
        self.rating =  (self.rating * self.num_ratings + rating) / (self.num_ratings + 1)
        self.num_ratings += 1
