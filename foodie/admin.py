from django.contrib import admin
from .models import UserProfile
from .models import Menu
from foodie.models import Order

class UserProfileAdminModel(admin.ModelAdmin):
    model = UserProfile
    list_display = ['id', 'user',  'money', 'warnings', 'certified','money_spent', 'num_orders']
    list_display_links = ["id", "user"]
    readonly_fields = ('user',)
    list_filter = ["certified"]
    search_fields = ['user__username']
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdminModel)


class MenuAdminModel(admin.ModelAdmin):
    list_display = ["name", "short_description", "price", "rating", "created_by"]
    list_display_links = ["name", "created_by"]
    list_filter = ["name", "rating", "created_by"]
    search_fields = ["name", "created_by"]
    class Meta:
        model = Menu

admin.site.register(Menu, MenuAdminModel)


class OrderAdminModel(admin.ModelAdmin):
    list_display = ["id", "date", "customer", "total", "delivered_by"]
    list_display_links = ["id", "date"]
    list_filter = ["date", "customer", "delivered_by"]
    search_fields = ["date", "customer", "total", "delivered_by"]
    class Meta:
        model = Order

admin.site.register(Order, OrderAdminModel)
