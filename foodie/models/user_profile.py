from django.db import models
from django.contrib.auth.models import User, Group

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

    def update(self, total):
        self.num_orders +=1
        self.money_spent += total
        self.money -= total
        if ((self.money_spent > 500 or self.num_orders > 50)):
            vip, created = Group.objects.get_or_create(name='vip')
            self.user.groups.add(vip)
            self.user.save()

    def is_vip(self):
        return self.user.groups.filter(name="vip").exists()

    def demote_vip(self):
        if self.is_vip():
            vip = Group.objects.get(name='vip')
            vip.user_set.remove(self.user)
            vip.save()


    def warn(self):
        self.warnings += 1
        if self.warnings == 2 and self.is_vip():
            self.demote_vip()
            self.warnings = 0
        elif self.warnings >= 3:
            self.user.is_active = False
            self.user.save()
