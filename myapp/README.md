User Authentication System
This is a user authentication system built with Django that allows users to log in using their email and password. It includes functionality for capturing a profile image using the webcam for enhanced security.

Features
User login with email and password.
Webcam access for capturing profile images.
Image verification using DeepFace.
CSRF protection for secure form submissions.
User profile image storage.
Installation
Prerequisites
Python 3.x
Django 5.1.1
DeepFace library
TensorFlow (with tf-keras)
OpenCV (for webcam access)
Setup
Clone the repository:

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Install required packages:

bash
Copy code
pip install django deepface tensorflow tf-keras opencv-python
Create and apply migrations:

bash
Copy code
python manage.py migrate
Start the development server:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/login/.

Usage
Navigate to the login page.
Enter your email and password.
Click the "Capture Image" button to take a picture using your webcam.
Submit the form to log in.
Important Notes
Ensure that your webcam is enabled and accessible.
The application uses CSRF tokens for security; make sure your requests include the CSRF token.
If you encounter issues with image verification, ensure that the DeepFace library is correctly installed and configured.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or features.

License
This project is licensed under the MIT License. See the LICENSE file for details.

