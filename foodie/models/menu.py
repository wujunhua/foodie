from django.db import models
from django.conf import settings # for ForeignKey on created_by
from main.models import Employee
from math import floor
#
#   ##############################  MENU  ######################################
#
class Menu(models.Model):
    name = models.CharField(max_length=50)
    short_description = models.TextField(default="")
    long_description = models.TextField(default="")
    price = models.IntegerField()
    vip_price = models.IntegerField(default=0)
    rating = models.DecimalField(default=0.0, max_digits=3, decimal_places=2) #might not need this field
    num_ratings = models.IntegerField(default=0) #might not need this field
    times_ordered = models.IntegerField(default=0)
    image_url = models.URLField(default="")
    on_menu = models.BooleanField(default=True)#Instead of deleting we just flip on_menu to false so it doesn't break relationships
    created_by = models.ForeignKey(
            Employee,
            on_delete=models.CASCADE,
            limit_choices_to={'user__groups__name' : 'chef'},
            default=1,
            #null=True,     # USEFUL TO UNCOMMENT AND COMMENT DEFAULT WHEN IMPORTING MENU ITEMS
    )

    def __str__(self):
        return self.name

    def update_rating(self, rating):
        self.rating =  (self.rating * self.num_ratings + rating) / (self.num_ratings + 1)
        self.num_ratings += 1

    def save(self, *args, **kwargs):
        self.vip_price = floor(self.price * .9)
        super(Menu, self).save(*args, **kwargs)
