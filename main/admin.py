from django.contrib import admin

# Register your models here.
from .models import Employee

class EmployeeModelAdmin(admin.ModelAdmin):
    def active(self, obj):
        if obj.user.is_active:
            return True
        else:
            return False
    get_user_active.boolean = True

    list_display = ["id", "first_name", "last_name", "salary", "demotions_remaining", "rating", "active"]
    list_filter = ["rating", "user__first_name", "user__is_active"]

    search_fields = ["id", "first_name", "last_name"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    class Meta:
        model = Employee
admin.site.register(Employee, EmployeeModelAdmin)
