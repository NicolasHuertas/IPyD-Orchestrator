import requests
import logging
from reservations.models import Reservation
from django.db import transaction

FLIGHT_SERVICE_URL = 'http://apigateway:8005/seats/'
HOTEL_SERVICE_URL = 'http://apigateway:8005/hotels/'

def create_combined_reservation(flight_data, hotel_data):
    headers = {'Content-Type': 'application/json'}
    with transaction.atomic():
        try:
            flight_response = requests.post(FLIGHT_SERVICE_URL, json=flight_data, headers=headers)
            if flight_response.status_code != 201:
                return None
            flight_reservation_id = flight_response.json()['id']
            print(flight_reservation_id)

            hotel_response = requests.post(HOTEL_SERVICE_URL, json=hotel_data, headers=headers)
            if hotel_response.status_code != 201:
                logging.info(f"Attempting to delete flight reservation ID: {flight_reservation_id}")
                delete_response = requests.delete(f"{FLIGHT_SERVICE_URL}{flight_reservation_id}/", headers=headers)
                if delete_response.status_code != 204:
                    logging.error(f"Failed to delete flight reservation ID: {flight_reservation_id}. Status Code: {delete_response.status_code}")
                return None
            hotel_reservation_id = hotel_response.json()['id']
        except requests.exceptions.RequestException as e:
            logging.error(f"Network or request error occurred: {e}")
            return None

        reservation = Reservation(hotel_reservation_id=hotel_reservation_id, flight_reservation_id=flight_reservation_id)
        reservation.save()
        return reservation

def cancel_combined_reservation(reservation_id):
    headers = {'Content-Type': 'application/json'}
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return False

    try:
        flight_cancel_response = requests.post(f"{FLIGHT_SERVICE_URL}{reservation.flight_reservation_id}/cancel/")
        hotel_cancel_response = requests.put(f"{HOTEL_SERVICE_URL}{reservation.hotel_reservation_id}/", json={'status': 'cancelled'})

        if flight_cancel_response.status_code == 201 and hotel_cancel_response.status_code == 200:
            reservation.cancelled = True
            reservation.save()
            return True
        else:
            if flight_cancel_response.status_code == 201:
                # Attempt to revert hotel cancellation if flight was cancelled successfully
                requests.put(f"{HOTEL_SERVICE_URL}{reservation.hotel_reservation_id}/", json={'status': 'active'})
            if hotel_cancel_response.status_code == 200:
                # Attempt to revert flight cancellation if hotel was cancelled successfully
                requests.post(f"{FLIGHT_SERVICE_URL}{reservation.flight_reservation_id}/cancel/")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Network or request error occurred: {e}")
        return False
