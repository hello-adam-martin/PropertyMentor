from rest_framework import generics
from properties.models import Property
from .serializers import PropertySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime

class PropertyList(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetail(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

@api_view(['GET'])
def check_availability(request, pk):
    property = get_object_or_404(Property, pk=pk)
    check_in = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')

    if not check_in or not check_out:
        return Response({"error": "Please provide check_in and check_out dates"}, status=400)

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    try:
        property.check_booking_rules(check_in_date, check_out_date)
        return Response({"available": True})
    except Exception as e:
        return Response({"available": False, "reason": str(e)})