import face_recognition
import cv2
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Profile
from django.core.files.storage import default_storage

def compare_faces_with_profile(request, username):
    """
    Compare a user's profile picture with a face extracted from an uploaded video.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the profile to fetch.

    Returns:
        JsonResponse: A JSON response indicating whether the faces match or an error occurred.
    """
    if request.method == "POST":
        try:
            # Fetch the user's profile based on the username
            profile = get_object_or_404(Profile, username=username)

            # Check if the user has a profile picture
            if not profile.profile_picture:
                return JsonResponse({"error": "Profile picture not available for this user."}, status=400)

            # Retrieve the path to the profile picture
            profile_picture_path = profile.profile_picture.path

            # Retrieve the uploaded video file
            video = request.FILES.get("video")
            if not video:
                return JsonResponse({"error": "No video file uploaded."}, status=400)

            # Save the uploaded video temporarily
            video_path = default_storage.save("tmp/video.mp4", video)

            try:
                # Load the profile picture and extract its face encoding
                profile_picture = face_recognition.load_image_file(profile_picture_path)
                profile_encodings = face_recognition.face_encodings(profile_picture)
                if not profile_encodings:
                    return JsonResponse({"error": "No face detected in the profile picture."}, status=400)

                profile_encoding = profile_encodings[0]

                # Extract a single frame from the uploaded video
                video_capture = cv2.VideoCapture(video_path)
                success, frame = video_capture.read()
                video_capture.release()

                if not success:
                    return JsonResponse({"error": "Unable to extract a frame from the video."}, status=400)

                # Convert the frame from BGR (OpenCV format) to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Extract face encodings from the video frame
                frame_encodings = face_recognition.face_encodings(frame_rgb)
                if not frame_encodings:
                    return JsonResponse({"error": "No face detected in the video frame."}, status=400)

                frame_encoding = frame_encodings[0]

                # Compare the faces
                results = face_recognition.compare_faces([profile_encoding], frame_encoding)
                is_match = results[0]

                return JsonResponse({"match": is_match})
            finally:
                # Ensure temporary files are cleaned up
                default_storage.delete(video_path)

        except Exception as e:
            # Catch any unexpected errors
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    # Handle invalid request methods
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
