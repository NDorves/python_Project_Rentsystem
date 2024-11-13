from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rent_booking_apps.listings.views import ListingViewSet

router = DefaultRouter()
router.register('listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
