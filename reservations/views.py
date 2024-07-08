from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import create_combined_reservation, cancel_combined_reservation

@api_view(['POST'])
def create_reservation(request):
    """
    Create a combined flight and hotel reservation.
    """
    reservation_date = request.data.get('reservation_date')
    flight_data = request.data.get('flight_data')
    hotel_data = request.data.get('hotel_data')

    if not (reservation_date and flight_data and hotel_data):
        return Response({'error': 'Missing data for reservation'}, status=status.HTTP_400_BAD_REQUEST)

    reservation = create_combined_reservation(reservation_date, flight_data, hotel_data)
    if reservation:
        return Response({'message': 'Reservation created successfully', 'reservation_id': reservation.id}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to create reservation'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete_reservation(request):
    """
    Cancel a combined flight and hotel reservation.
    """
    reservation_id = request.data.get('reservation_id')

    if not reservation_id:
        return Response({'error': 'Missing reservation ID'}, status=status.HTTP_400_BAD_REQUEST)

    if cancel_combined_reservation(reservation_id):
        return Response({'message': 'Reservation cancelled successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to cancel reservation'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)