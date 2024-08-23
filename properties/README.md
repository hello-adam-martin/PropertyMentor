# Property App

This Django app manages properties and their pricing rules for the Short Term Rental Property Management system.

## Features

- Create, read, update, and delete properties
- Manage complex pricing rules for each property
- Calculate property prices based on date and applicable rules

## Models

### Property

- `name`: CharField - Name of the property
- `address`: TextField - Address of the property
- `owner`: ForeignKey to Owner model
- `bedrooms`: PositiveIntegerField - Number of bedrooms
- `bathrooms`: DecimalField - Number of bathrooms
- `max_occupancy`: PositiveIntegerField - Maximum number of occupants
- `nightly_rate`: DecimalField - Base nightly rate
- `description`: TextField - Property description
- `date_added`: DateField - Date when the property was added to the system

#### Methods

- `get_price_for_date(date)`: Calculates the price for a specific date based on applicable pricing rules

### PricingRule

- `property`: ForeignKey to Property model
- `rule_type`: CharField - Type of pricing rule (weekend, seasonal, holiday)
- `start_date`: DateField - Start date for seasonal and holiday rules
- `end_date`: DateField - End date for seasonal rules
- `price_modifier`: DecimalField - Percentage modifier for the base price

#### Methods

- `get_modifier_factor()`: Returns the price modifier as a decimal factor

## Pricing Logic

The system supports three types of pricing rules:

1. Weekend Pricing: Applied to Fridays and Saturdays
2. Seasonal Pricing: Applied to a date range
3. Holiday Pricing: Applied to a specific date

Rules are applied in the following order of precedence:
1. Holiday
2. Seasonal
3. Weekend

The base nightly rate is used if no rules apply.

## Usage

To create a new property:

1. Go to the admin interface
2. Click on "Properties" under the "Properties" app
3. Click "Add Property"
4. Fill in the required information
5. Save the property

To add pricing rules to a property:

1. Edit the property in the admin interface
2. Scroll to the "Pricing rules" section
3. Click "Add another Pricing rule"
4. Choose the rule type and fill in the details
5. Save the property

## Admin Customizations

The admin interface is customized to:
- Display key property information in the list view
- Allow inline editing of pricing rules when editing a property
- Show pricing rules with clear percentage representations

## Future Enhancements

- Implement a public-facing property listing interface
- Add support for property images
- Implement a calendar view to visualize pricing over time
- Add support for amenities and property features