# Short Term Rental Property Management API

This API provides comprehensive access to the Short Term Rental Property Management system. It allows authenticated users to manage properties, bookings, and perform various operations related to short-term rentals, as well as subscribe to webhooks for real-time notifications.

## Table of Contents

1. [Base URL](#base-url)
2. [Authentication](#authentication)
3. [Pagination](#pagination)
4. [Filtering and Searching](#filtering-and-searching)
5. [Endpoints](#endpoints)
   - [Properties](#properties)
   - [Bookings](#bookings)
   - [Owners](#owners)
   - [Webhooks](#webhooks)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Webhooks](#webhooks-1)
9. [Usage Examples](#usage-examples)
10. [Development Setup](#development-setup)
11. [Testing](#testing)
12. [Future Enhancements](#future-enhancements)
13. [Support](#support)
14. [License](#license)

## Base URL

All URLs referenced in the documentation have the following base:

```
http://localhost:8000/api/
```

## Authentication

The API uses token-based authentication. To use the API, you need to include an authentication token in the header of your requests:

```
Authorization: Token your_token_here
```

### Obtaining a Token

To obtain a token, make a POST request to the token endpoint:

- URL: `/api/token/`
- Method: `POST`
- Data Params: 
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Success Response:
  - Code: 200
  - Content: 
    ```json
    {
      "token": "your_auth_token",
      "user_id": 1,
      "email": "user@example.com"
    }
    ```

Once you have obtained a token, include it in the Authorization header of all subsequent requests.

## Pagination

List endpoints support pagination using the following query parameters:

- `page`: The page number to retrieve
- `page_size`: The number of items per page (default is 10, max is 100)

## Filtering and Searching

The property list endpoint supports filtering and searching:

- Filter by: `bedrooms`, `bathrooms`, `max_occupancy`
- Search fields: `name`, `address`
- Ordering: `nightly_rate`, `date_added`

Example:
```
GET /api/properties/?bedrooms=2&search=beach&ordering=-nightly_rate
```

## Endpoints

### Properties

#### List All Properties

- URL: `/properties/`
- Method: `GET`
- URL Params: 
  - Optional: `page=[integer]`
  - Optional: `page_size=[integer]`
- Success Response: 200 OK

#### Get Property Details

- URL: `/properties/<id>/`
- Method: `GET`
- URL Params: 
  - Required: `id=[integer]`
- Success Response: 200 OK

#### Create Property

- URL: `/properties/create/`
- Method: `POST`
- Data Params: Property details (name, address, owner, etc.)
- Success Response: 201 Created

#### Update Property

- URL: `/properties/<id>/update/`
- Method: `PUT`
- URL Params:
  - Required: `id=[integer]`
- Data Params: Updated property details
- Success Response: 200 OK

#### Check Property Availability

- URL: `/properties/<id>/check-availability/`
- Method: `GET`
- URL Params:
  - Required: `id=[integer]`
  - Required: `check_in=[date]`
  - Required: `check_out=[date]`
- Success Response: 200 OK

#### Search Properties

- URL: `/properties/search/`
- Method: `GET`
- URL Params:
  - Optional: `location=[string]`
  - Optional: `min_bedrooms=[integer]`
  - Optional: `max_bedrooms=[integer]`
  - Optional: `min_price=[decimal]`
  - Optional: `max_price=[decimal]`
- Success Response: 200 OK

#### Get Property Pricing

- URL: `/properties/<id>/pricing/`
- Method: `GET`
- URL Params:
  - Required: `id=[integer]`
  - Required: `check_in=[date]`
  - Required: `check_out=[date]`
  - Required: `guests=[integer]`
- Success Response: 200 OK

### Bookings

#### Create Booking

- URL: `/bookings/`
- Method: `POST`
- Data Params: Booking details (property, guest, dates, etc.)
- Success Response: 201 Created

#### Get Booking Details

- URL: `/bookings/<id>/`
- Method: `GET`
- URL Params:
  - Required: `id=[integer]`
- Success Response: 200 OK

#### Update Booking

- URL: `/bookings/<id>/update/`
- Method: `PUT`
- URL Params:
  - Required: `id=[integer]`
- Data Params: Updated booking details
- Success Response: 200 OK

#### Cancel Booking

- URL: `/bookings/<id>/cancel/`
- Method: `POST`
- URL Params:
  - Required: `id=[integer]`
- Success Response: 200 OK

### Owners

#### Get Owner Properties

- URL: `/owners/<owner_id>/properties/`
- Method: `GET`
- URL Params:
  - Required: `owner_id=[integer]`
- Success Response: 200 OK

#### Owner Booking Overview

- URL: `/owners/<owner_id>/bookings/`
- Method: `GET`
- URL Params:
  - Required: `owner_id=[integer]`
- Success Response: 200 OK

### Webhooks

#### List Available Webhook Events

- URL: `/webhooks/events/`
- Method: `GET`
- Success Response: 200 OK

#### List and Create Webhook Subscriptions

- URL: `/webhooks/`
- Method: `GET` (list) or `POST` (create)
- Data Params (for POST):
  ```json
  {
    "event": "booking_created",
    "target_url": "https://your-server.com/webhook-endpoint"
  }
  ```
- Success Response: 200 OK (GET) or 201 Created (POST)

#### Manage Specific Webhook Subscription

- URL: `/webhooks/<id>/`
- Method: `GET` (retrieve), `PUT` (update), or `DELETE` (delete)
- URL Params:
  - Required: `id=[integer]`
- Success Response: 200 OK (GET/PUT) or 204 No Content (DELETE)

## Error Handling

The API uses standard HTTP response codes to indicate the success or failure of requests:

- 2xx codes indicate success
- 4xx codes indicate an error that failed given the information provided
- 5xx codes indicate an error with our servers

Detailed error messages are provided in the response body.

## Rate Limiting

To prevent abuse, API requests are subject to rate limiting. The current limits are:

- 1000 requests per hour for authenticated users
- 100 requests per hour for unauthenticated users

## Webhooks

The API supports webhooks for real-time notifications of certain events.

### Available Webhook Events

- `booking_created`: Triggered when a new booking is created
- `booking_updated`: Triggered when an existing booking is updated
- `booking_cancelled`: Triggered when a booking is cancelled
- `property_created`: Triggered when a new property is added
- `property_updated`: Triggered when a property's details are updated

### Webhook Payload

When an event occurs, the API will send a POST request to the subscribed `target_url` with the following payload:

```json
{
  "event": "booking_created",
  "payload": {
    // Event-specific data
  }
}
```

## Usage Examples

1. Obtain an authentication token:
   ```
   POST /api/token/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. List all properties:
   ```
   GET /api/properties/
   Header: Authorization: Token your_token_here
   ```

3. Get details for property with ID 1:
   ```
   GET /api/properties/1/
   Header: Authorization: Token your_token_here
   ```

4. Check availability for property with ID 1:
   ```
   GET /api/properties/1/check-availability/?check_in=2024-07-01&check_out=2024-07-05
   Header: Authorization: Token your_token_here
   ```

5. Search for beachfront properties:
   ```
   GET /api/properties/search/?location=beach&min_bedrooms=2&max_price=300
   Header: Authorization: Token your_token_here
   ```

6. Get pricing for property with ID 1:
   ```
   GET /api/properties/1/pricing/?check_in=2024-07-01&check_out=2024-07-05&guests=2
   Header: Authorization: Token your_token_here
   ```

7. Create a new booking:
   ```
   POST /api/bookings/
   Header: Authorization: Token your_token_here
   {
     "property": 1,
     "guest": 1,
     "check_in_date": "2024-07-01",
     "check_out_date": "2024-07-05",
     "num_guests": 2
   }
   ```

8. Cancel booking with ID 1:
   ```
   POST /api/bookings/1/cancel/
   Header: Authorization: Token your_token_here
   ```

9. List available webhook events:
   ```
   GET /api/webhooks/events/
   Header: Authorization: Token your_token_here
   ```

10. Create a webhook subscription:
    ```
    POST /api/webhooks/
    Header: Authorization: Token your_token_here
    {
      "event": "booking_created",
      "target_url": "https://your-server.com/webhook-endpoint"
    }
    ```

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

## Testing

Run the test suite using:

```
python manage.py test
```

## Future Enhancements

- Implement user roles and permissions
- Add support for multiple currencies
- Implement a review and rating system for properties
- Add support for property amenities and features
- Implement dynamic pricing based on demand and seasonality

## Support

For any questions or issues, please contact the development team at [dev-team@example.com](mailto:dev-team@example.com).

## License

[Specify your license here]

---

This API documentation is subject to change as new features are added or existing ones are modified. Always refer to the latest version of this document for the most up-to-date information.