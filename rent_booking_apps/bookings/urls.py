from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rent_booking_apps.bookings.views import BookingViewSet

router = DefaultRouter()
router.register('', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
