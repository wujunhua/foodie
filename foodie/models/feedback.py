from django.db import models
from main.models import Employee
from . import UserProfile

class Feedback(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.TextField()

    CMPMENT = "compliment"
    CMPLAINT = "complaint"

    FEEDBACK_TYPE_CHOICES = (
            (CMPMENT, "Compliment"),
            (CMPLAINT, "Complaint"),
            )
    feedback_type = models.CharField(choices=FEEDBACK_TYPE_CHOICES, default=CMPLAINT, max_length=20)
    manager_seen = models.BooleanField(default=False)
