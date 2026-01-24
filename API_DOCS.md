# API Documentation (example)

## Endpoints

- `/` (GET): Home page
- `/auth/login` (GET, POST): User login
- `/auth/register` (GET, POST): User registration
- `/booking/search` (GET): Search for hotels
- `/booking/book/confirm` (GET): Confirm booking
- `/booking/book/create` (POST): Create booking (server-side price calculation)
- `/booking/my-bookings` (GET): View user's bookings
- `/booking/receipt/<booking_id>` (GET): View booking receipt
- `/booking/cancel/<booking_id>` (GET, POST): Cancel booking
- `/admin/` (GET): Admin dashboard
- `/admin/users` (GET): Manage users
- `/admin/currencies` (GET): Manage currencies
- `/admin/hotels` (GET): Manage hotels
- `/admin/reports` (GET): Sales reports

## Notes

- All POST endpoints require CSRF protection (enabled via Flask-WTF).
- Admin endpoints require admin login.
- All templates should extend `base.html`.
