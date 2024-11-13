from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rent_booking_apps.reviews.views import ReviewViewSet

router = DefaultRouter()
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
