from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from properties.models import Property
from bookings.models import Booking
from owners.models import Owner
from .models import WebhookSubscription
from .serializers import PropertySerializer, BookingSerializer, WebhookSubscriptionSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PropertyList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bedrooms', 'bathrooms', 'max_occupancy']
    search_fields = ['name', 'address']
    ordering_fields = ['nightly_rate', 'date_added']

class PropertyDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_availability(request, pk):
    property = get_object_or_404(Property, pk=pk)
    check_in = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')

    if not check_in or not check_out:
        return Response({"error": "Please provide check_in and check_out dates"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        property.check_booking_rules(check_in_date, check_out_date)
        return Response({"available": True})
    except Exception as e:
        return Response({"available": False, "reason": str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_properties(request):
    location = request.query_params.get('location')
    min_bedrooms = request.query_params.get('min_bedrooms')
    max_bedrooms = request.query_params.get('max_bedrooms')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    queryset = Property.objects.all()

    if location:
        queryset = queryset.filter(Q(address__icontains=location) | Q(name__icontains=location))
    if min_bedrooms:
        queryset = queryset.filter(bedrooms__gte=min_bedrooms)
    if max_bedrooms:
        queryset = queryset.filter(bedrooms__lte=max_bedrooms)
    if min_price:
        queryset = queryset.filter(nightly_rate__gte=min_price)
    if max_price:
        queryset = queryset.filter(nightly_rate__lte=max_price)

    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PropertySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def property_pricing(request, pk):
    property = get_object_or_404(Property, pk=pk)
    check_in = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')
    guests = request.query_params.get('guests')

    if not check_in or not check_out or not guests:
        return Response({"error": "Please provide check_in, check_out dates, and number of guests"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        num_guests = int(guests)
    except ValueError:
        return Response({"error": "Invalid date format or number of guests. Use YYYY-MM-DD for dates and an integer for guests"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = Booking(property=property, check_in_date=check_in_date, check_out_date=check_out_date, num_guests=num_guests)
        booking.clean()  # This will calculate the price
        return Response({
            "total_price": booking.total_price,
            "base_total": booking.base_total,
            "fees_total": booking.fees_total
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookingCreate(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingDetail(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingUpdate(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == 'cancelled':
        return Response({"error": "This booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = 'cancelled'
    booking.save()
    return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_owner_properties(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    properties = Property.objects.filter(owner=owner)
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(properties, request)
    serializer = PropertySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_booking_overview(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    properties = Property.objects.filter(owner=owner)
    bookings = Booking.objects.filter(property__in=properties).order_by('check_in_date')
    
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(bookings, request)
    serializer = BookingSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

class WebhookEventsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = WebhookSubscription.get_available_events()
        return Response(events)

class WebhookSubscriptionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebhookSubscriptionSerializer

    def get_queryset(self):
        return WebhookSubscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        events = WebhookSubscription.get_available_events()
        return Response({
            'available_events': events,
            'subscriptions': serializer.data
        })

class WebhookSubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebhookSubscriptionSerializer

    def get_queryset(self):
        return WebhookSubscription.objects.filter(user=self.request.user)
    
