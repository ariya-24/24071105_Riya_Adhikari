# SECURITY.md

## Security Best Practices

- Never trust client input for sensitive operations (e.g., price, user roles).
- Always recalculate prices and validate all user input on the server.
- Use HTTPS in production and set secure cookie flags.
- Store secrets and credentials in environment variables, not in code or version control.
- Keep all dependencies up to date to avoid vulnerabilities.
- Use CSRF protection for all forms (Flask-WTF is enabled).
- Set session timeouts and use secure session cookies.
- Regularly review logs for suspicious activity.

## Reporting Vulnerabilities

If you discover a security issue, please report it privately to the project maintainer.
