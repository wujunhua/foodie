from django.db import models
from django.conf import settings # for ForeignKey on created_by
from main.models import Employee
from foodie.models import UserProfile
from foodie.models import Menu

#   #############################  ORDER  ######################################
#
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
            UserProfile,
            on_delete=models.CASCADE,
            default=1,
    )
    address = models.TextField(default="")
    total = models.IntegerField()
    frozen = models.BooleanField(default=False)
    delivered_by = models.ForeignKey(
            Employee,
            on_delete=models.CASCADE,
            limit_choices_to={'user__groups__name' : 'driver'},
            null=True,
    )
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " - " + self.customer.user.username

    def item_set(self):
        return OrderItem.objects.filter(order_id=self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    food_rating = models.FloatField(default=0.0)
    delivery_rating = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.item.rating = (self.item.rating * self.item.num_ratings + self.food_rating) / (self.item.num_ratings + 1)
        self.item.num_ratings += 1
        self.item.save()

        super(OrderItem, self).save(*args, **kwargs)
