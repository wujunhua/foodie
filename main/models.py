from django.db import models
from django.contrib.auth.models import User, Group
from decimal import *       # for decimal casting in demote() function

#
#   ############################  EMPLOYEE  ####################################
#
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Instead of using a choice field. We can just put this user into a "manager", "chef", "driver" Group
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=25000.00)

    rating = models.SmallIntegerField(default=0)
    complaints = models.SmallIntegerField(default=0)
    compliments = models.SmallIntegerField(default=0)
    certified = models.BooleanField(default=False)

    demotions_remaining = models.SmallIntegerField(default=2)

    def __str__(self):
        return self.user.username

    def demote(self, percentage, menu_items):       # pass percent as 20 for 20%
        if (self.demotions_remaining > 0):
            self.salary = self.salary - (self.salary * (Decimal(percentage) * Decimal(.01)))
            self.demotions_remaining -= 1
        else:
            for item in menu_items:
                item.on_menu = False
                item.save()
            self.demotions_remaining -= 1
            self.user.is_active = False
            self.user.save()

    def promote(self, percentage):      # pass percent as 20 for 20%
        self.salary = self.salary + (self.salary * (Decimal(percentage) * Decimal(.01)))

    def got_complaint(self, menu_items):
        self.complaints += 1
        if self.complaints == 3:
            self.demote(15, menu_items)
            self.complaints = 0

    def got_compliment(self):
        if self.complaints > 0:
            self.complaints -= 1
        else:
            self.compliments += 1

        if self.compliments == 3:
            self.promote(15)
            self.compliments = 0
