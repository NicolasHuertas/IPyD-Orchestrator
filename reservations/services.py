import requests
from django.db import transaction
from .models import Reservation

FLIGHT_SERVICE_URL = 'http://localhost:8005/flights/' 
HOTEL_SERVICE_URL = 'http://localhost:8005/hotels/'  

def create_combined_reservation(reservation_date, flight_data, hotel_data):
    with transaction.atomic():
        # Attempt to create flight reservation
        flight_response = requests.post(FLIGHT_SERVICE_URL, json=flight_data)
        if flight_response.status_code == 200:
            flight_reservation_id = flight_response.json()['id']
        else:
            # Delete hotel reservation if flight reservation fails
            requests.delete(f"{HOTEL_SERVICE_URL}{hotel_data['id']}/")
            return None

        # Attempt to create hotel reservation
        hotel_response = requests.post(HOTEL_SERVICE_URL, json=hotel_data)
        if hotel_response.status_code == 200:
            hotel_reservation_id = hotel_response.json()['id']
        else:
            # Delete flight reservation if hotel reservation fails
            requests.delete(f"{FLIGHT_SERVICE_URL}{flight_data['id']}/")
            return None

        # If both reservations are successful, save the combined reservation
        reservation = Reservation(
            hotel_reservation_id=hotel_reservation_id,
            flight_reservation_id=flight_reservation_id
        )
        reservation.save()
        return reservation

def cancel_combined_reservation(reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    # Attempt to cancel flight reservation using POST request
    flight_cancel_response = requests.post(f"{FLIGHT_SERVICE_URL}{reservation.flight_reservation_id}/cancel")
    flight_cancelled = flight_cancel_response.status_code == 200

    # Attempt to cancel hotel reservation
    hotel_cancel_response = requests.put(f"{HOTEL_SERVICE_URL}{reservation.hotel_reservation_id}/", json={'status': 'cancelled'})
    hotel_cancelled = hotel_cancel_response.status_code == 200

    # Check if either cancellation failed
    if flight_cancelled and not hotel_cancelled:
        # Set flight reservation back to active
        requests.put(f"{FLIGHT_SERVICE_URL}{reservation.flight_reservation_id}/", json={'status': 'active'})
        return False
    elif hotel_cancelled and not flight_cancelled:
        # Set hotel reservation back to active
        requests.put(f"{HOTEL_SERVICE_URL}{reservation.hotel_reservation_id}/", json={'status': 'active'})
        return False

    if flight_cancelled and hotel_cancelled:
        # If both cancellations are successful, update the reservation status to 'cancelled'
        reservation.cancelled = True
        reservation.save()
        return True
    else:
        return False