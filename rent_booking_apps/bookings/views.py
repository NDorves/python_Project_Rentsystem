from rest_framework import generics, viewsets, permissions
from rent_booking_apps.bookings.models import Booking, BookingStatus
from rent_booking_apps.bookings.serializers import BookingSerializer
from rent_booking_apps.listings.serializers import ChoicesSerializer


class PropertyTypeListView(generics.ListAPIView):
    queryset = BookingStatus.choices
    serializer_class = ChoicesSerializer
    pagination_class = None


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

