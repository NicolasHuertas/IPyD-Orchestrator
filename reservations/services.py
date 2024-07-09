import requests
from django.db import transaction
from .models import Reservation

FLIGHT_SERVICE_URL = 'http://flight-service/api/reservations/'  # Unchanged
HOTEL_SERVICE_URL = 'http://localhost:8005/hotels/'  # Updated URL

def create_combined_reservation(reservation_date, flight_data, hotel_data):
    with transaction.atomic():
        # Attempt to create flight reservation
        flight_response = requests.post(f"{FLIGHT_SERVICE_URL}create/", json=flight_data)
        if flight_response.status_code == 200:
            flight_reservation_id = flight_response.json()['reservation_id']
        else:
            # Handle failure
            return None

        # Attempt to create hotel reservation
        hotel_response = requests.post(HOTEL_SERVICE_URL, json=hotel_data)  # Simplified URL
        if hotel_response.status_code == 200:
            hotel_reservation_id = hotel_response.json()['id']
        else:
            # If hotel reservation fails, cancel the flight reservation
            requests.post(f"{FLIGHT_SERVICE_URL}cancel/", json={'reservation_id': flight_reservation_id})
            return None

        # If both reservations are successful, save the combined reservation
        reservation = Reservation(
            reservation_date=reservation_date,
            hotel_reservation_id=hotel_reservation_id,
            flight_reservation_id=flight_reservation_id,
            status='active'
        )
        reservation.save()
        return reservation

def cancel_combined_reservation(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    # Cancel flight reservation
    flight_cancel_response = requests.post(f"{FLIGHT_SERVICE_URL}cancel/", json={'reservation_id': reservation.flight_reservation_id})
    if flight_cancel_response.status_code != 200:
        # Handle failure
        return False

    # Cancel hotel reservation
    hotel_cancel_response = requests.put(f"{HOTEL_SERVICE_URL}{reservation.hotel_reservation_id}/", json={'status': 'cancelled'})
    if hotel_cancel_response.status_code != 200:
        # If hotel cancellation fails, consider rebooking the flight or handling it accordingly
        return False

    # Update reservation status
    reservation.status = 'cancelled'
    reservation.save()
    return True