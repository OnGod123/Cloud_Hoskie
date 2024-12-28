import base64
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login  # Import Django's authenticate and login functions
from .models import User_login
from myapp.models import Person
from django.core.files.base import ContentFile
from deepface import DeepFace  # Import DeepFace for image comparison

def login_view(request):
    if request.method == 'GET':
        # Render the login page
        return render(request, 'login.html')
    
    if request.method == 'POST':
        try:
            username_or_email = request.POST.get('username_or_email')  # Field for either username or email
            password = request.POST.get('password')
            profile_image_data = request.POST.get('profile_image_data')  # Base64 image content (optional)
            profile_image_filename = request.POST.get('profile_image_filename')  # Image filename (optional)

            # Validate input fields
            if not username_or_email or not password:
                return JsonResponse({'success': False, 'message': 'Username/email and password are required'}, status=400)

            # Try to find the user by username or email
            person = None

            # Check if the input is a username or email and filter accordingly
            if '@' in username_or_email:
                person = Person.objects.filter(email=username_or_email).first()
            else:
                person = Person.objects.filter(username=username_or_email).first()

            if not person:
                return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

            # Authenticate the user using Django's authenticate() function
            user = authenticate(request, username=person.username, password=password)

            if user is not None:
                # Log in the user using Django's login() function
                login(request, user)

                # Log in user to custom User_login model
                user_login, created = User_login.objects.get_or_create(person=person)

                # Handle the image data if provided
                if profile_image_data and profile_image_filename:
                    try:
                        # Extract file extension from the filename
                        ext = profile_image_filename.split('.')[-1]  # Extract file extension
                        filename = f"profiles/{person.name}_{person.username}.{ext}"  # Create unique filename

                        # Save the image to the media directory
                        image_content = ContentFile(base64.b64decode(profile_image_data), name=filename)
                        new_image_path = os.path.join('media', filename)
                        user_login.profile_image.save(filename, image_content, save=True)
                    except Exception as e:
                        return JsonResponse({'success': False, 'message': f'Error saving profile image: {str(e)}'}, status=500)

                # Increment login count
                user_login.increment_login_count()

                # Check for image verification on subsequent logins if an image is uploaded
                if user_login.login_count > 1 and profile_image_data:
                    stored_image_path = user_login.profile_image.path

                    try:
                        # Use DeepFace to compare images
                        result = DeepFace.verify(new_image_path, stored_image_path)

                        if result['verified']:
                            # If verification is successful, set verified to True
                            user_login.verified = True
                        else:
                            return JsonResponse({'success': False, 'message': 'Image verification failed'}, status=403)
                    except Exception as e:
                        return JsonResponse({'success': False, 'message': f'Error during image verification: {str(e)}'}, status=500)

                user_login.start_session()  # Start session
                user_login.save()

                # Redirect to the home page after successful login
                return redirect('home')
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

