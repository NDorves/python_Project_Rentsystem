from rest_framework import viewsets, permissions

from rent_booking_apps.reviews.models import Review
from rent_booking_apps.reviews.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

