from django.urls import path, include

urlpatterns = [
    path('', include('rent_booking_apps.users.urls')),
    path('', include('rent_booking_apps.bookings.urls')),
    path('', include('rent_booking_apps.listings.urls')),
    path('', include('rent_booking_apps.reviews.urls')),
    ]
