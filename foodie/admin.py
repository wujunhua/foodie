from django.contrib import admin
from .models import UserProfile

class UserProfileAdminModel(admin.ModelAdmin):
    model = UserProfile
    list_display = ['id', 'user',  'money', 'warnings_allowed', 'certified','money_spent', 'num_orders']
    readonly_fields = ('user',)
    list_filter = ["certified"]
    search_fields = ['user__username']


admin.site.register(UserProfile, UserProfileAdminModel)
