from django.db import models
from decimal import *       # for decimal casting in demote() function

#
#   ############################  EMPLOYEE  ####################################
#
class Employee(models.Model):
    # ************ CONSTANTS *************
    CHEF = 'CH'
    DRVR = 'DD'
    MNGR = 'MG'

    ACTIVE = 'AC'
    INACTV = 'IN'
    # ************ CONSTANTS *************

    employee_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=70)

    POSITION_CHOICES = (
        (CHEF, 'Chef'),
        (DRVR, 'Delivery Driver'),
        (MNGR, 'Manager'),
    )
    position = models.CharField(max_length=4, choices=POSITION_CHOICES, default=DRVR)

    salary = models.DecimalField(max_digits=8, decimal_places=2, default=25000.00)

    # 0 = neutral
    rating = models.SmallIntegerField(default=0)
    complaints = models.SmallIntegerField(default=0)

    demotions_remaining = models.SmallIntegerField(default=2)

    ACTIVE_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTV, 'Inactive'),
    )
    active = models.CharField(max_length=6, choices=ACTIVE_CHOICES, default=ACTIVE)


    def __str__(self):
        return self.full_name

    def is_active(self):
        return self.active == 'AC'

    def demote(self, percentage):       # pass percent as 20 for 20%
        if (self.demotions_remaining > 0):
            self.salary = self.salary - (self.salary * (Decimal(percentage) * Decimal(.01)))
            self.demotions_remaining -= 1
        else:
            self.demotions_remaining -= 1
            self.active = 'IN'

    def promote(self, percentage):      # pass percent as 20 for 20%
        self.salary = self.salary + (self.salary * (Decimal(percentage) * Decimal(.01)))

    def got_complaint(self):
        self.complaints += 1
        if self.complaints == 3:
            self.demote()
            self.complaints = 0

    def got_compliment(self):
        self.complaints -= 1
        if self.complaints == -3:
            self.promote()
            self.complaints = 0
