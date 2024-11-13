from rest_framework import serializers

from rent_booking_apps.reviews.models import Review
from rent_booking_apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing_url = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

