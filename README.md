# Django Authentication System

## Features
- User registration
- Login with username/email
- Password reset using Django's built-in views
- Password change
- Dashboard
- Profile page

## Setup
1. Clone the repository
2. Install Django: `pip install django`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## Authentication Flow
- Users can sign up with username and email
- Login using username or email
- Reset password via email (console backend for development)
  - Request password reset
  - Receive reset link via email
  - Set new password
- Change password when logged in
- View profile details
- Logout option available

## Notes
- Uses Django's built-in authentication system and class-based views
- Minimal styling (focus on functionality)
- Development email backend (prints password reset emails to console)
