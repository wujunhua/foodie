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
        self.money_spent += cart.toal
        self.money -= cart.total
        self.save()

        if ((self.money_spent > 500 or self.num_orders > 50)):
            self.promote_vip()

    def promote_vip(self):
        vip, created = Group.objects.get_or_create(name='vip')
        self.user.groups.add(group)
        self.user.save()


