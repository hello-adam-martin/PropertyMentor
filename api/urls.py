from django.urls import path
from .views import (
    PropertyList, PropertyDetail, PropertyCreate, PropertyUpdate,
    check_availability, search_properties, property_pricing,
    BookingCreate, BookingDetail, BookingUpdate, cancel_booking,
    get_owner_properties, owner_booking_overview,
    WebhookSubscriptionList, WebhookSubscriptionDetail, WebhookEventsList
)
from .auth import CustomAuthToken

urlpatterns = [
    # Property-related URLs
    path('properties/', PropertyList.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetail.as_view(), name='property-detail'),
    path('properties/create/', PropertyCreate.as_view(), name='property-create'),
    path('properties/<int:pk>/update/', PropertyUpdate.as_view(), name='property-update'),
    path('properties/<int:pk>/check-availability/', check_availability, name='check-availability'),
    path('properties/search/', search_properties, name='search-properties'),
    path('properties/<int:pk>/pricing/', property_pricing, name='property-pricing'),

    # Booking-related URLs
    path('bookings/', BookingCreate.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/update/', BookingUpdate.as_view(), name='booking-update'),
    path('bookings/<int:pk>/cancel/', cancel_booking, name='cancel-booking'),

    # Owner-related URLs
    path('owners/<int:owner_id>/properties/', get_owner_properties, name='owner-properties'),
    path('owners/<int:owner_id>/bookings/', owner_booking_overview, name='owner-booking-overview'),

    # Authentication URL
    path('token/', CustomAuthToken.as_view(), name='api_token_auth'),

    # Webhook-related URLs
    path('webhooks/events/', WebhookEventsList.as_view(), name='webhook-events'),
    path('webhooks/', WebhookSubscriptionList.as_view(), name='webhook-list'),
    path('webhooks/<int:pk>/', WebhookSubscriptionDetail.as_view(), name='webhook-detail'),
]