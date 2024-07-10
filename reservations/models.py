from django.db import models
from django.utils import timezone

class Reservation(models.Model):
    reservation_date = models.DateField(default=timezone.now)
    hotel_reservation_id = models.CharField(max_length=255)
    flight_reservation_id = models.CharField(max_length=255)
    cancelled = models.BooleanField(default=False)
