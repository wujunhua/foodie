from django.db import models
from django.contrib.auth.models import User

#Maybe need a complaints field?
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=0)
    warnings = models.IntegerField(default=0)
    num_orders = models.IntegerField(default=0)
    money_spent = models.IntegerField(default=0)
    certified  = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def is_vip(self):
        return ((self.money_spent > 500 or self.num_orders > 50))

