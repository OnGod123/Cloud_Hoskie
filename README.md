Django Project: User Registration and Social Login
Overview
This Django project provides a user registration system with the following features:

Standard Email/Password Login: Users can log in with their email and password.
Social Authentication: Users can log in using their social media accounts (e.g., Facebook, Google, Instagram).
User Data Submission: A form to collect user details such as name, relationship status, birth date, etc.
Email Notifications: After registration, the system sends a welcome email to the user.
Features
Home Page: A simple home page that welcomes users.
User Registration: Users can submit their personal details and register on the platform.
Email Notification: After a successful registration, a welcome email is sent to the registered user.
Social Login: Users can log in with popular social media platforms (Facebook, Google, Instagram).
Logging: The project logs important events such as user registration and email sending status.
Setup
Prerequisites
Python 3.x
Django 3.x or newer
A PostgreSQL or SQLite database (depending on your settings)
Email server credentials for sending notifications (e.g., SMTP server)
Installation
Clone the repository:

bash
Copy code
git clone n https://github.com/OnGod123/Cloud_Hoskie.git
cd Cloud_Hoskie
Create a virtual environment and activate it:

bash
Copy code
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Set up your database:

If using PostgreSQL, ensure it's installed and running, then create the necessary database:
sql
Copy code
CREATE DATABASE mydatabase;
Run database migrations:

bash
Copy code
python manage.py migrate
Set up your email backend in the settings.py file for sending registration emails:

python
Copy code
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
Configure social authentication (e.g., Facebook, Google, Instagram) in the settings.py file using packages like django-allauth.

Running the Application
Start the Django development server:

bash
Copy code
python manage.py runserver
Access the application by navigating to http://127.0.0.1:8000/ in your browser.

Project Structure
php
Copy code
myapp/
├── templates/
│   ├── index.html            # Main index page
│   ├── login.html            # Login page with email/password and social login options
│   └── base.html             # Base template for consistent styling
├── static/
│   ├── css/
│   │   └── styles.css        # CSS styles
│   └── js/
│       └── scripts.js        # JavaScript files
├── models.py                 # Person model for user details
├── views.py                  # Handles form submissions and rendering pages
├── urls.py                   # Routes for handling login, social login, etc.
└── emails.py                 # Email sending functionality
Key Files
models.py: Defines the Person model to store user information such as name, email, relationship status, etc.
views.py: Handles requests for login, registration, and user submission. Integrates social login and email notifications.
emails.py: A helper function to send a welcome email after user registration.
Notable Functionalities
User Registration Form
Users fill out a registration form with fields such as name, relationship status, sexual orientation, phone number, and more. The form data is then validated and stored in the database.

Social Login
The project integrates social login options using django-allauth. The login template provides links for social login through providers like Facebook, Google, and Instagram.

Email Notifications
After successful registration, the user receives a welcome email. The email is sent using Django's email backend, which you can configure in the settings.py file.

Future Enhancements
Password Reset: Add functionality for users to reset their passwords.
Profile Management: Allow users to edit their profile information after registering.
Multi-factor Authentication: Implement MFA for enhanced security.
Logging
The project uses Python's built-in logging module to log important events like user registration, errors during email sending, etc.

Contributing
If you'd like to contribute to this project, please feel free to fork the repository and submit a pull request.

License
This project is licensed under the MIT License.

Usage
To log in with your email and password, visit the login page: https://yourdomain.com/login/.
To register, visit the registration page: https://yourdomain.com/signup/.
To log in with a social account, select the appropriate provider from the login page.





