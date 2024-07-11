from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import create_combined_reservation, cancel_combined_reservation
from .models import Reservation 
from .serializers import ReservationSerializer  

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['POST'])
def create_reservation(request):
    """
    Create a combined flight and hotel reservation. 
    """
    flight_data = request.data.get('flight_data')
    hotel_data = request.data.get('hotel_data')

    if not (flight_data and hotel_data):
        return Response({'error': 'Missing data for reservation'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            reservation = create_combined_reservation(flight_data, hotel_data)
            if reservation:
                return Response({'message': 'Reservation created successfully', 'reservation_id': reservation.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Failed to create reservation', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def cancel_reservation(request):
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