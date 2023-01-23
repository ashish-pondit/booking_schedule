from django.db import models


# Create your models here.
class DliiliUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    user_type = models.CharField(max_length=10, null=True)

    class Meta:
        abstract = True


class Guide(DliiliUser):
    price = models.PositiveIntegerField(default=50, null=True)


class Tourist(DliiliUser):
    country = models.CharField(max_length=100, null=True)
