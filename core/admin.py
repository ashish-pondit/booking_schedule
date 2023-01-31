from django.contrib import admin
from .models import Guide, Tourist, Booking
# Register your models here.
admin.site.register(Guide)
admin.site.register(Tourist)
admin.site.register(Booking)