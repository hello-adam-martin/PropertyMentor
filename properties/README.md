# Properties App

This Django app manages properties and their associated rules for the Short Term Rental Property Management system.

## Features

- Create, read, update, and delete properties
- Manage complex pricing rules for each property
- Define booking rules including minimum stay requirements
- Support for gap stays
- Flexible check-in and check-out day restrictions
- Fee management system with support for incorporated and separate fees
- Calculate property prices based on date, applicable rules, and fees

## Models

### Property

- Basic information: name, address, owner, bedrooms, bathrooms, max occupancy, etc.
- `nightly_rate`: Base nightly rate
- `allow_gap_stays`: Boolean to allow bookings shorter than the minimum stay to fill gaps
- `no_checkin_days`: Days when check-in is not allowed
- `no_checkout_days`: Days when check-out is not allowed
- `minimum_stay`: Default minimum number of nights for a booking

#### Key Methods

- `get_price_for_date(date)`: Calculates the price for a specific date based on applicable pricing rules
- `check_booking_rules(check_in_date, check_out_date)`: Validates a booking against all applicable booking rules

### PricingRule

- `property`: ForeignKey to Property model
- `rule_type`: Type of pricing rule (weekend, seasonal, override)
- `start_date` and `end_date`: Date range for the rule (if applicable)
- `price_modifier`: Percentage modifier for the base price

### BookingRule

- `property`: ForeignKey to Property model
- `start_date` and `end_date`: Date range for the rule
- `min_nights`: Minimum number of nights required for bookings in this date range

### Fee

- `property`: ForeignKey to Property model
- `name`: Name of the fee
- `fee_type`: Type of fee (percentage or fixed amount)
- `amount`: Amount of the fee
- `applies`: How the fee applies (per night or once per stay)
- `display_strategy`: How the fee should be displayed (incorporated into nightly rate or shown separately)
- `is_extra_guest_fee`: Boolean indicating if this is an extra guest fee
- `extra_guest_threshold`: Number of guests above which the extra guest fee applies

## Pricing Logic

The system supports three types of pricing rules:

1. Override Pricing: Applied to a specific date (e.g., holidays, special events)
2. Seasonal Pricing: Applied to a date range
3. Weekend Pricing: Applied to specific days of the week (typically Friday and Saturday)

Rules are applied in the following order of precedence:
1. Override (highest priority)
2. Seasonal
3. Weekend
4. Base nightly rate (lowest priority)

## Fee Logic

Fees can be:
- Percentage-based or fixed amount
- Applied per night or once per stay
- Incorporated into the nightly rate or displayed separately
- Applied as extra guest fees above a certain number of guests

## Booking Rules

The system supports several types of booking rules:

1. No Check-in Days: Prevents check-ins on specific days of the week
2. No Check-out Days: Prevents check-outs on specific days of the week
3. Minimum Stay: Sets a default minimum number of nights for bookings
4. Date-specific Minimum Stay: Sets a minimum number of nights for bookings during a specific date range

Gap stays are supported if enabled for a property, allowing bookings shorter than the minimum stay to fill gaps between existing bookings.

## Admin Customizations

The admin interface is customized to:
- Display key property information in the list view
- Allow inline editing of pricing rules, booking rules, and fees when editing a property
- Show pricing rules with clear percentage representations
- Provide an intuitive interface for setting no check-in and no check-out days
- Allow easy management of fees, including their display strategy

## Usage

To create a new property with rules and fees:

1. Go to the admin interface
2. Click on "Properties" under the "Properties" app
3. Click "Add Property"
4. Fill in the basic property information
5. Set the default minimum stay and select any no check-in/check-out days
6. In the inline sections, add pricing rules, date-specific minimum stay rules, and fees as needed
7. Save the property

## Future Enhancements

- Implement a public-facing property listing interface
- Add support for property images
- Implement a calendar view to visualize pricing and availability over time
- Add support for amenities and property features
- Develop a more sophisticated gap stay pricing strategy
- Implement dynamic pricing based on demand and occupancy rates