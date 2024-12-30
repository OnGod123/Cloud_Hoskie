from django.conf import settings
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .videos_model import Video
from myapp.models import Person

# Render the video page
def render_page(request):
    """
    Renders the page to upload or capture video.
    """
    return render(request, 'video_page.html')


def upload_video(request):
    """
    Handle video upload by saving the file to the server and storing metadata in the database.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)

    # Check for the required video file
    if not request.FILES.get('video_file'):
        return JsonResponse({'error': 'No video file provided'}, status=400)

    # Validate 'person_id' in the request
    person_id = request.POST.get('person_id')
    if not person_id:
        return JsonResponse({'error': 'Person ID is required'}, status=400)

    try:
        # Attempt to fetch the person object
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return JsonResponse({'error': 'Person not found'}, status=404)

    video_file = request.FILES['video_file']
    video_title = request.POST.get('title', 'Untitled')

    # Save the video file to the server
    upload_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
    try:
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)  # Ensure the directory exists
        with open(upload_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)
    except Exception as e:
        return JsonResponse({'error': f'Error saving video file: {str(e)}'}, status=500)

    try:
        # Save the video metadata to the database
        video = Video.objects.create(
            person=person,
            video_file=f'videos/{video_file.name}',  # Save the relative file path
            title=video_title
        )
    except ValidationError as e:
        return JsonResponse({'error': f'Validation error: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Video uploaded successfully', 'video_id': video.id})


def capture_video(request):
    """
    Handle video capture by simulating capture logic and saving the metadata.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)

    # Validate 'person_id' in the request
    person_id = request.POST.get('person_id')
    if not person_id:
        return JsonResponse({'error': 'Person ID is required'}, status=400)

    try:
        # Attempt to fetch the person object
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return JsonResponse({'error': 'Person not found'}, status=404)

    # Capture video logic (stubbed for now)
    title = request.POST.get('title', 'Captured Video')

    # Example capture file path
    capture_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'captured_video.mp4')
    try:
        with open(capture_path, 'wb') as f:
            f.write(b"")  # Simulate an empty video file (replace with actual capture logic)
    except Exception as e:
        return JsonResponse({'error': f'Error saving captured video: {str(e)}'}, status=500)

    try:
        # Save captured video metadata to the database
        video = Video.objects.create(
            person=person,
            video_file='videos/captured_video.mp4',
            title=title
        )
    except ValidationError as e:
        return JsonResponse({'error': f'Validation error: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Video captured successfully', 'video_id': video.id})
