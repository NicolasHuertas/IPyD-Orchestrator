from django.db import models

class Reservation(models.Model):
    reservation_date = models.DateField()
    hotel_reservation_id = models.CharField(max_length=255)
    flight_reservation_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
