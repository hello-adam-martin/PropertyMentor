# Bookings App

This Django app manages bookings for the Short Term Rental Property Management system.

## Features

- Create, read, update, and delete bookings
- Automatic price calculation based on property nightly rate and booking duration
- Booking validation to prevent conflicts and ensure logical date ranges
- Admin interface for managing bookings

## Models

### Booking

- `property`: ForeignKey to Property model
- `guest`: ForeignKey to Guest model
- `check_in_date`: Date of check-in
- `check_out_date`: Date of check-out
- `total_price`: Automatically calculated based on property rate and duration
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `booking_date`: Date when the booking was created
- `special_requests`: Text field for any special requests

## Validation Rules

1. Check-out date must be after check-in date
2. Check-out date cannot be the same as check-in date
3. Bookings cannot overlap with existing bookings for the same property
4. A booking can start on the same day as another booking checks out

## Price Calculation

The total price is automatically calculated based on the property's nightly rate and the number of nights booked.

## Admin Interface

The admin interface provides a customized view for managing bookings:

- List display shows key booking information
- Filters for status and dates
- Search functionality
- Read-only total price field
- Custom titles for list, add, and edit views

## Usage

To create a new booking:

1. Go to the admin interface
2. Click on "Bookings" under the "Bookings" app
3. Click "Add Booking"
4. Fill in the required information
5. Save the booking

The system will automatically validate the booking and calculate the total price.

## Future Enhancements

- Implement a public-facing booking interface
- Add email notifications for booking status changes
- Integrate with a payment system
- Implement more complex pricing rules (e.g., weekend rates, seasonal pricing)