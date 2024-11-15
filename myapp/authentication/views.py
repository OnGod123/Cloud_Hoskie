import json
import base64
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
            profile_image_data = request.POST.get('profile_image')  # Base64 image data (optional)

            # Try to find the user by username or email
            person = None

            # Check if the input is a username or email and filter accordingly
            if '@' in username_or_email:
                person = Person.objects.filter(email=username_or_email).first()
            else:
                person = Person.objects.filter(username=username_or_email).first()

            if person and person.check_password(password):
                # Log in user
                user_login, created = User_login.objects.get_or_create(person=person)

                # Handle the base64 image if provided
                if profile_image_data:
                    # Decode the base64 image
                    format, imgstr = profile_image_data.split(';base64,')  # Split out the metadata
                    ext = format.split('/')[-1]  # Extract file extension
                    filename = f"profiles/{person.name}_{person.username}.{ext}"  # Create unique filename

                    # Save the image to the media directory
                    image_content = ContentFile(base64.b64decode(imgstr), name=filename)
                    new_image_path = os.path.join('media', filename)
                    user_login.profile_image.save(filename, image_content, save=True)

                # Increment login count
                user_login.increment_login_count()
                
                if user_login.login_count > 1 and profile_image_data:
                    # Compare the newly uploaded image with the stored image
                    stored_image_path = user_login.profile_image.path

                    # Use DeepFace to compare images
                    result = DeepFace.verify(new_image_path, stored_image_path)

                    if result['verified']:
                        # If verification is successful, set verified to True
                        user_login.verified = True
                    else:
                        return JsonResponse({'success': False, 'message': 'Image verification failed'}, status=403)

                user_login.start_session()  # Start session
                user_login.save()

                # Redirect to the home page after successful login
                return redirect('home')
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
