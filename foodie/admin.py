from django.contrib import admin
from .models import UserProfile
from .models import Menu
from foodie.models import Order, OrderItem, Feedback
from main.models import Employee

class UserProfileAdminModel(admin.ModelAdmin):
    model = UserProfile
    list_display = ['id', 'user',  'money', 'warnings', 'certified','money_spent', 'num_orders']
    list_display_links = ["id", "user"]
    readonly_fields = ('user',)
    list_filter = ["certified", "warnings"]
    search_fields = ['user__username']
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdminModel)


class MenuAdminModel(admin.ModelAdmin):
    list_display = ["name", "short_description", "price", "rating", "created_by"]
    list_display_links = ["name", "created_by"]
    readonly_fields = ('rating', 'num_ratings', 'times_ordered', 'vip_price')
    list_filter = ["name", "rating", "created_by"]
    search_fields = ["name", "created_by"]

    def get_queryset(self, request):
        qs = super(MenuAdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        employee = Employee.objects.filter(user=request.user).first()
        return qs.filter(created_by=employee)
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

class OrderItemAdminModel(admin.ModelAdmin):
    list_display = ["id", "order", "item", "quantity", "subtotal", "food_rating", "delivery_rating"]
    list_filter =["order", "item"]
    search_fields = ["id", "order", "item"]
    class Meta:
        model = OrderItem
admin.site.register(OrderItem, OrderItemAdminModel)

class FeedbackAdminModel(admin.ModelAdmin):
    list_display = ["id", "customer", "employee", "feedback", "feedback_type"]
    class Meta:
        model= Feedback
admin.site.register(Feedback, FeedbackAdminModel)
