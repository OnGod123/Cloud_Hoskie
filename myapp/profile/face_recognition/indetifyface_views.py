from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import Profile
import face_recognition
import numpy as np
import logging

# Configure logging for debugging purposes
logger = logging.getLogger(__name__)

def identify_person(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"error": "No image file provided."}, status=400)

    # Save the uploaded image temporarily
    temp_path = default_storage.save("tmp/captured_image.jpg", image_file)

    try:
        # Load the uploaded image and compute its face encoding
        uploaded_image = face_recognition.load_image_file(temp_path)
        uploaded_encodings = face_recognition.face_encodings(uploaded_image)

        if not uploaded_encodings:
            return JsonResponse({"error": "No face detected in the uploaded image."}, status=400)

        uploaded_encoding = uploaded_encodings[0]

        # Retrieve profiles with existing face encodings
        profiles = Profile.objects.exclude(face_encoding=None)

        # Compare the uploaded encoding with stored encodings
        for profile in profiles:
            try:
                stored_encoding = np.array(profile.face_encoding)
                match = face_recognition.compare_faces([stored_encoding], uploaded_encoding, tolerance=0.6)

                if match[0]:
                    return JsonResponse(
                        {
                            "person_id": profile.person.id,
                            "username": profile.username,
                        }
                    )
            except Exception as e:
                logger.error(f"Error while comparing faces for profile {profile.id}: {e}")

        return JsonResponse({"error": "No match found."}, status=404)
    except Exception as e:
        logger.error(f"Error in identify_person: {e}")
        return JsonResponse({"error": "An error occurred while processing the image."}, status=500)
    finally:
        # Cleanup temporary files
        default_storage.delete(temp_path)
