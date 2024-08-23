# Bookings App

This Django app manages bookings for the Short Term Rental Property Management system.

## Features

- Create, read, update, and delete bookings
- Automatic price calculation based on property pricing rules
- Booking validation to prevent conflicts and ensure logical date ranges
- Support for gap stays (shorter stays that fill gaps between existing bookings)
- Admin interface for managing bookings

## Models

### Booking

- `property`: ForeignKey to Property model
- `guest`: ForeignKey to Guest model
- `check_in_date`: Date of check-in
- `check_out_date`: Date of check-out
- `total_price`: Automatically calculated based on property pricing rules
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `booking_date`: Date when the booking was created
- `special_requests`: Text field for any special requests

## Key Methods

- `calculate_price_breakdown()`: Calculates the price for each night of the stay
- `get_price_and_rule_for_date()`: Determines the price for a specific date based on pricing rules
- `calculate_total_price()`: Computes the total price for the entire stay
- `clean()`: Performs validation checks including overlapping bookings and adherence to booking rules

## Validation Rules

1. Check-out date must be after check-in date
2. Bookings cannot overlap with existing bookings for the same property
3. Bookings must adhere to the property's booking rules:
   - No check-ins on restricted days
   - No check-outs on restricted days
   - Minimum stay requirement (either default or date-specific)
4. Gap stays are allowed if the property permits them

## Price Calculation

The total price is automatically calculated based on the property's pricing rules, which can include:

- Base nightly rate
- Weekend pricing
- Seasonal pricing
- Override pricing for specific dates

## Admin Interface

The admin interface provides a customized view for managing bookings:

- List display shows key booking information
- Filters for status and dates
- Search functionality
- Read-only total price field
- Price breakdown display

## Usage

To create a new booking:

1. Go to the admin interface
2. Click on "Bookings" under the "Bookings" app
3. Click "Add Booking"
4. Fill in the required information
5. Save the booking

The system will automatically validate the booking, apply relevant pricing rules, and calculate the total price.

## Interaction with Property App

The Booking app relies on the Property app for:
- Property information
- Pricing rules
- Booking rules (minimum stay, no check-in/check-out days, gap stay settings)

Ensure that properties and their rules are correctly set up in the Property app for accurate booking calculations and validations.

## Future Enhancements

- Implement a public-facing booking interface
- Add email notifications for booking status changes
- Integrate with a payment system
- Implement a calendar view to visualize available dates and pricing
- Develop a more sophisticated gap stay handling system