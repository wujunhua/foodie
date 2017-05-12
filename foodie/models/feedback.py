from django.db import models
from main.models import Employee
from .models import UserProfile

class Feedback(models.Model):
    customer = models.ForeingKey(UserProfile, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.TextField()

    CMPMENT = "ment"
    CMPLAINT = "aint"

    FEEDBACK_TYPE_CHOICES = (
            (CMPMENT, "Compliment"),
            (CMPLAINT, "Complaint"),
            )
    feedback_type = models.CharField(choices=FEEDBACK_TYPE_CHOICES, default=CMPLAINT)
    manager_seen = models.BooleanField(default=False)
