# Short Term Rental Property Management API

This API provides access to the Short Term Rental Property Management system. It allows users to retrieve property information and check property availability.

## Base URL

All URLs referenced in the documentation have the following base:

```
http://localhost:8000/api/
```

## Endpoints

### List All Properties

Retrieves a list of all properties in the system.

- URL: `/properties/`
- Method: `GET`
- URL Params: None
- Success Response:
  - Code: 200
  - Content: Array of property objects
    ```json
    [
      {
        "id": 1,
        "name": "Seaside Villa",
        "address": "123 Ocean Drive",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "max_occupancy": 6,
        "nightly_rate": "250.00",
        "description": "Beautiful villa with ocean views"
      },
      ...
    ]
    ```

### Get Property Details

Retrieves details for a specific property.

- URL: `/properties/<id>/`
- Method: `GET`
- URL Params: 
  - Required: `id=[integer]`
- Success Response:
  - Code: 200
  - Content: Property object
    ```json
    {
      "id": 1,
      "name": "Seaside Villa",
      "address": "123 Ocean Drive",
      "bedrooms": 3,
      "bathrooms": 2.5,
      "max_occupancy": 6,
      "nightly_rate": "250.00",
      "description": "Beautiful villa with ocean views"
    }
    ```
- Error Response:
  - Code: 404
  - Content: `{ "detail": "Not found." }`

### Check Property Availability

Checks if a property is available for the specified dates.

- URL: `/properties/<id>/check-availability/`
- Method: `GET`
- URL Params:
  - Required: `id=[integer]`
  - Required: `check_in=[date]`
  - Required: `check_out=[date]`
- Success Response:
  - Code: 200
  - Content: 
    ```json
    {
      "available": true
    }
    ```
    or
    ```json
    {
      "available": false,
      "reason": "Booking does not meet minimum stay requirement of 3 nights."
    }
    ```
- Error Response:
  - Code: 400
  - Content: `{ "error": "Please provide check_in and check_out dates" }`
  or
  - Code: 400
  - Content: `{ "error": "Invalid date format. Use YYYY-MM-DD" }`
  or
  - Code: 404
  - Content: `{ "detail": "Not found." }`

## Usage Examples

Here are some example API calls you can make using a web browser:

1. List all properties:
   ```
   http://localhost:8000/api/properties/
   ```

2. Get details for property with ID 1:
   ```
   http://localhost:8000/api/properties/1/
   ```

3. Check availability for property with ID 1 from July 1, 2024, to July 5, 2024:
   ```
   http://localhost:8000/api/properties/1/check-availability/?check_in=2024-07-01&check_out=2024-07-05
   ```

## Notes

- Dates should be in the format YYYY-MM-DD.
- The API currently doesn't require authentication, but this should be implemented before deploying to production.
- For POST, PUT, or DELETE requests, you'll need to use a tool like Postman or cURL, as browsers primarily send GET requests.

## Future Enhancements

- Add endpoints for creating, updating, and deleting properties
- Implement user authentication and authorization
- Add endpoints for managing bookings and guests
- Implement filtering and pagination for the property list endpoint

For any questions or issues, please contact the development team.