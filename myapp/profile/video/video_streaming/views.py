from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from myapp.profile.video.videos_model import Video
import base64

def video_stream_view(request):
    return render(request, 'video_stream.html')

@csrf_exempt
def share_video(request, video_id):
    """
    Endpoint to retrieve Base64 encoded video data for sharing.
    """
    try:
        video = get_object_or_404(Video, id=video_id)
        video_path = video.video_file.path

        with open(video_path, 'rb') as video_file:
            encoded_video = base64.b64encode(video_file.read()).decode('utf-8')

        return JsonResponse({"video_id": video_id, "video_data": encoded_video, "title": video.title})
    except FileNotFoundError:
        return JsonResponse({"error": "Video file not found."}, status=404)
    except Exception as e:
        # Log the error here if needed
        return JsonResponse({"error": "An error occurred while processing the video."}, status=500)
