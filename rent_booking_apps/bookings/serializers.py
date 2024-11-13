from rest_framework import serializers

from rent_booking_apps.bookings.models import Booking
from rent_booking_apps.users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    booking_url = serializers.SerializerMethodField()
    listing_url = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

        read_only_fields = [
            'user', 'price', 'status', 'created_at', 'updated_at'
        ]


