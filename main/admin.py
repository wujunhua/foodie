from django.contrib import admin

# Register your models here.
from .models import Employee

class EmployeeModelAdmin(admin.ModelAdmin):
    def active(self, obj):
        if obj.user.is_active:
            return True
        else:
            return False
    active.boolean = True

    list_display = ["id", "username", "first_name", "last_name", "salary", "demotions_remaining", "rating", "active", "certified", "position"]
    list_filter = ["rating", "user__first_name", "user__is_active", "certified"]
    list_display_links = ['id', 'username']

    search_fields = ["id", "first_name", "last_name"]

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def position(self, obj):
        if obj.user.groups.filter(name="chef").exists():
            return "chef"
        elif obj.user.groups.filter(name="driver").exists():
            return "driver"
        else:
            return "manager"

    class Meta:
        model = Employee
admin.site.register(Employee, EmployeeModelAdmin)
