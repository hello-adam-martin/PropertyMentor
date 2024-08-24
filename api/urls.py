from django.urls import path
from .views import PropertyList, PropertyDetail, check_availability

urlpatterns = [
    path('properties/', PropertyList.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetail.as_view(), name='property-detail'),
    path('properties/<int:pk>/check-availability/', check_availability, name='check-availability'),
]