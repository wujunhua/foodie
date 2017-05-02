from django.contrib import admin

# Register your models here.
from .models import Employee

class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "full_name", "position", "salary", "demotions_remaining", "rating", "active"]
    list_display_links = ["full_name"]
    list_filter = ["position", "rating", "active"]

    search_fields = ["full_name"]
    class Meta:
        model = Employee

admin.site.register(Employee, EmployeeModelAdmin)
