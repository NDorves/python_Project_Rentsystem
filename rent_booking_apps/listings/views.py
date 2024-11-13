from rest_framework import generics, viewsets, permissions, filters
from rent_booking_apps.listings.models import PropertyType, Listing
from rent_booking_apps.listings.serializers import ChoicesSerializer, ListingSerializer


class PropertyTypeListView(generics.ListAPIView):
    queryset = PropertyType.choices
    serializer_class = ChoicesSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
    