from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from myapp.models import Person
from .image_models import Image
import os
import base64
from io import BytesIO
from PIL import Image as PILImage

# Render the image upload page
def render_image_page(request):
    return render(request, 'image_page.html')

# Handle image uploads (from file input)
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        try:
            person = Person.objects.get(id=request.POST['person_id'])
        except Person.DoesNotExist:
            return JsonResponse({'error': 'Person not found'}, status=404)

        image_file = request.FILES['image_file']

        # Save the file using Django's FileSystemStorage
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        # Save the image metadata in the database
        image = Image.objects.create(
            person=person,
            image_file=uploaded_file_url,  # Save the relative path for the DB
            caption=request.POST.get('caption', 'No caption')
        )
        return JsonResponse({'message': 'Image uploaded successfully', 'image_id': image.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Handle captured image upload (from webcam capture)
def capture_image(request):
    if request.method == 'POST':
        person_id = request.POST.get('person_id')
        caption = request.POST.get('caption')
        image_data = request.POST.get('image_data')

        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return JsonResponse({'error': 'Person not found'}, status=404)

        # Decode the Base64 image data (strip off the prefix if present)
        image_data = image_data.split(',')[1]  # Remove the base64 prefix
        image_bytes = base64.b64decode(image_data)
        image = PILImage.open(BytesIO(image_bytes))

        # Generate a unique filename for the image
        image_filename = f'captured_image_{person_id}_{str(os.urandom(6).hex())}.jpg'
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_filename)

        # Ensure the images directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)

        # Save the image metadata in the database
        image_instance = Image.objects.create(
            person=person,
            image_file=f'images/{image_filename}',  # Relative path for the DB
            caption=caption
        )

        return JsonResponse({'message': 'Image captured and uploaded successfully', 'image_id': image_instance.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)
