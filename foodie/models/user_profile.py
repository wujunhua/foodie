from django.db import models
from django.contrib.auth.models import User

#Maybe need a complaints field?
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=0)
    warnings_allowed = models.IntegerField(default=3)
    num_orders = models.IntegerField(default=0)
    money_spent = models.IntegerField(default=0)
    is_certified  = models.BooleanField(default=False)
