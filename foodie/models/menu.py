from django.db import models
from django.conf import settings # for ForeignKey on created_by
from main.models import Employee
#
#   ##############################  MENU  ######################################
#
class Menu(models.Model):
    name = models.CharField(max_length=50)
    short_description = models.TextField(default="")
    long_description = models.TextField(default="")
    price = models.IntegerField()
    rating = models.FloatField(default=0.0) #might not need this field
    num_ratings = models.IntegerField(default=0) #might not need this field
    times_ordered = models.IntegerField(default=0)
    image_url = models.URLField(default="")
    on_menu = models.BooleanField(default=True)#Instead of deleting we just flip on_menu to false so it doesn't break relationships
    created_by = models.ForeignKey(
            Employee,
            on_delete=models.CASCADE,
            limit_choices_to={'position' : 'CH'},
            default=1,
    )

    def __str__(self):
        return self.name

    def update_rating(self, rating):
        self.rating =  (self.rating * self.num_ratings + rating) / (self.num_ratings + 1)
        self.num_ratings += 1
