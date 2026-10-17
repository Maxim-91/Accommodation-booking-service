# Accommodation Booking Service — API Contract

## 1. Purpose

This document defines the API contract between the frontend and backend of the Accommodation Booking Service. It describes the planned endpoints, request and response formats, authentication requirements, and error handling.

The API contract is agreed upon before implementing the endpoints. If the contract changes, the documentation and affected frontend/backend code must be updated.

## 2. General conventions

- API data is exchanged as JSON.
- The API base path is `/api/v1`.
- Dates use the `YYYY-MM-DD` format.
- Prices are expressed in EUR.
- Resource identifiers are integers.
- The backend is responsible for validating input and enforcing business rules.
- The backend identifies the authenticated user from the validated access token.
- Passwords and password hashes must never be returned in API responses.
- Internal server exceptions and stack traces must not be exposed to clients.

## 3. Accommodation endpoints

| Method | Endpoint                      | Description                    | Access |
| ------ | ----------------------------- | ------------------------------ | ------ |
| GET    | `/api/v1/accommodations`      | List and filter accommodations | Public |
| GET    | `/api/v1/accommodations/{id}` | Get accommodation details      | Public |

### Accommodation list filters

The list endpoint supports the following optional query parameters:

- `location`: location or city
- `minPrice`: minimum price per night
- `maxPrice`: maximum price per night
- `checkIn`: arrival date
- `checkOut`: departure date
- `guests`: number of guests

Example:

`GET /api/v1/accommodations?location=Helsinki&minPrice=50&maxPrice=150&guests=2`

Example response:

```json
{
  "items": [
    {
      "id": 12,
      "name": "Central apartment",
      "location": "Helsinki",
      "pricePerNight": 95,
      "currency": "EUR",
      "maxGuests": 3,
      "amenities": ["Wi-Fi", "Sauna"]
    }
  ],
  "total": 1
}
```

The backend must validate filter values. Date filters must check availability for the requested stay when availability filtering is implemented.

### Accommodation details

`GET /api/v1/accommodations/{id}` returns the selected accommodation's public details, including its description, location, price, capacity, and amenities.

If the accommodation does not exist, the API returns `404 Not Found`.

## 4. Authentication endpoints

| Method | Endpoint                | Description          | Access        |
| ------ | ----------------------- | -------------------- | ------------- |
| POST   | `/api/v1/auth/register` | Register a user      | Public        |
| POST   | `/api/v1/auth/login`    | Authenticate a user  | Public        |
| GET    | `/api/v1/auth/me`       | Get the current user | Authenticated |

### Registration request

```json
{
  "email": "traveller@example.com",
  "password": "example-password"
}
```

The response contains public user information only. It must not include the password or password hash.

### Login

The login endpoint accepts an email and password. On success, it returns an access token and its expiration information.

Authenticated requests use the following header:

`Authorization: Bearer <access-token>`

Invalid or missing authentication results in `401 Unauthorized`.

## 5. Booking endpoints

| Method | Endpoint                | Description                      | Access        |
| ------ | ----------------------- | -------------------------------- | ------------- |
| GET    | `/api/v1/bookings/me`   | List the current user's bookings | Authenticated |
| POST   | `/api/v1/bookings`      | Create a booking                 | Authenticated |
| DELETE | `/api/v1/bookings/{id}` | Cancel a booking                 | Authenticated |

### Create booking request

```json
{
  "accommodationId": 12,
  "checkIn": "2027-06-10",
  "checkOut": "2027-06-14",
  "guests": 2
}
```

The backend determines the booking owner from the access token; the client does not supply a trusted `userId`.

A successful creation returns `201 Created` and the created booking.

The backend must reject invalid date ranges, past bookings, excessive guest counts, unavailable accommodation, overlapping bookings where applicable, and unauthorized operations. Business rules are implemented in the service layer.

Users may view and cancel only their own bookings unless a documented administrative permission applies.

## 6. Error responses

Errors use a consistent JSON structure:

```json
{
  "status": 409,
  "code": "BOOKING_CONFLICT",
  "message": "The accommodation is not available for the selected dates."
}
```

The `code` is a stable application error identifier. The `message` is safe for the client to display.

| HTTP status | Meaning                                    |
| ----------- | ------------------------------------------ |
| 200         | Successful request                         |
| 201         | Resource created                           |
| 204         | Successful operation with no response body |
| 400         | Invalid request                            |
| 401         | Missing or invalid authentication          |
| 403         | Authenticated user lacks permission        |
| 404         | Resource not found                         |
| 409         | Business-rule or booking conflict          |
| 422         | Request data failed validation             |
| 500         | Unexpected server error                    |

The exact validation status codes must be implemented consistently and documented.

## 7. Scope and future extensions

This contract describes the initial API. Accommodation creation and editing, administrative endpoints, pagination, and additional features may be added when their requirements are confirmed.

The contract does not imply that every endpoint has already been implemented.

## 8. Acceptance criteria

- [x] Main accommodation, authentication, and booking endpoints are documented.
- [x] Request parameters and JSON examples are documented.
- [x] Authentication and ownership rules are defined.
- [x] HTTP status codes and error response structure are defined.
- [x] Frontend and backend can use this document as a shared reference.
- [x] The document is committed to the repository and reviewed through a pull request.
