from django.db import models
from schedule.models import Calendar


# Create your models here.
class BaseUserModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    user_type = models.CharField(max_length=10, null=True)

    class Meta:
        abstract = True


class Guide(BaseUserModel):
    price = models.PositiveIntegerField(default=50, null=True)
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return "Guide: {}".format(self.name)


class Tourist(BaseUserModel):
    country = models.CharField(max_length=100, null=True)

    # def __str__(self):
    #     return "Tourist: {}".format(self.name)


class Booking(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.SET_NULL, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
