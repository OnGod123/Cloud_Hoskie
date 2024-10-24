import json
import base64
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserProfile
from myapp.models import Person
from django.core.files.base import ContentFile
from deepface import DeepFace  # Import DeepFace for image comparison

def login_view(request):
    if request.method == 'GET':
        # Render the login page
        return render(request, 'login.html')
    
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            profile_image_data = request.POST.get('profile_image')  # Get the base64 image data

            # Verify user credentials
            person = Person.objects.filter(email=email).first()
            if person and person.check_password(password):
                # Log in user
                user_profile, created = UserProfile.objects.get_or_create(person=person)

                # Handle the base64 image if provided
                if profile_image_data:
                    # Decode the base64 image
                    format, imgstr = profile_image_data.split(';base64,')  # Split out the metadata
                    ext = format.split('/')[-1]  # Extract file extension
                    filename = f"profiles/{person.name}_{person.email}.{ext}"  # Create unique filename

                    # Save the image to the media directory
                    image_content = ContentFile(base64.b64decode(imgstr), name=filename)
                    new_image_path = os.path.join('media', filename)
                    user_profile.profile_image.save(filename, image_content, save=True)

                # Increment login count
                user_profile.increment_login_count()
                
                if user_profile.login_count > 1 and profile_image_data:
                    # Compare the newly uploaded image with the stored image
                    stored_image_path = user_profile.profile_image.path

                    # Use DeepFace to compare images
                    result = DeepFace.verify(new_image_path, stored_image_path)

                    if result['verified']:
                        # If verification is successful, set verified to True
                        user_profile.verified = True
                    else:
                        return JsonResponse({'success': False, 'message': 'Image verification failed'}, status=403)

                user_profile.start_session()  # Start session
                
                # Save user profile
                user_profile.save()

                # Redirect to the home page after successful login
                return redirect('home')
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
