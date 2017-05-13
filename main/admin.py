from django.contrib import admin

# Register your models here.
from .models import Employee

class EmployeeModelAdmin(admin.ModelAdmin):
    def get_user_active(self, obj):
        if obj.user.is_active:
            return True
        else:
            return False
    get_user_active.boolean = True

    list_display = ["id", "get_user_first_name", "get_user_last_name", "salary", "demotions_remaining", "rating", "get_user_active"]
    list_filter = ["rating", "user__first_name", "user__is_active"]

    search_fields = ["id", "get_user_first_name", "get_user_last_name"]

    def get_user_first_name(self, obj):
        return obj.user.first_name

    def get_user_last_name(self, obj):
        return obj.user.last_name

    class Meta:
        model = Employee
admin.site.register(Employee, EmployeeModelAdmin)
