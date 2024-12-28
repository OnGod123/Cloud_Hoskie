from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person
from .emails import send_welcome_email
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request): 

    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        return HttpResponse('Invalid request method.')

def create_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        relationship_status = request.POST.get('relationship_status')
        sexual_orientation = request.POST.get('sexual_orientation')
        race = request.POST.get('race')
        phone_number = request.POST.get('phone_number')
        social_media_api = request.POST.get('social_media_api')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(request.POST)

        # Check for required fields
        if not all([name, relationship_status, sexual_orientation, race,
                    phone_number, social_media_api, birth_date, email, password]):
            return HttpResponse('All fields are required.')

        # Save the data to the database
        person = Person(
            name=name,
            relationship_status=relationship_status,
            sexual_orientation=sexual_orientation,
            race=race,
            phone_number=phone_number,
            social_media_api=social_media_api,
            birth_date=birth_date,
            email=email,
            password=password
        )
        
        try:
            person.save()
            logger.info(f"Successfully saved person: {person.name}")
        except Exception as e:
            logger.error(f"Error saving person: {e}")
            return HttpResponse('An error occurred while processing your registration. Please try again later.')

        try:
            # Send welcome email to the user
            send_welcome_email(person.name, person.email)
            logger.info(f"Welcome email sent to {person.email}")
        except RuntimeError as e:
            logger.error(f"Error sending email: {e}")
            return HttpResponse('An error occurred while sending the welcome email. Please try again later.')
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            return HttpResponse('An unexpected error occurred while sending the welcome email. Please try again later.')

        return HttpResponse(f'Name: {name}, Email: {email}, Registration Successful. Check your email for a welcome message.')
    else:
        return HttpResponse('Invalid request method.')


from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp.models import Person
from myapp.profile.models import Profile  # Adjust the import path


def similar_profiles_view(request):
    """
    API view to return paginated similar profiles for subscribed users,
    excluding the current user. Adds profile image to the response data.
    """
    try:
        # Ensure the user is authenticated and subscribed
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=401)

        if not hasattr(request.user, 'profile') or not request.user.profile.is_subscribed:
            return JsonResponse({"error": "You must be subscribed to view this data."}, status=403)

        current_user = request.user.person  # Assuming a relation from Profile to Person
        sexual_orientation = current_user.sexual_orientation

        # Get query parameters for pagination
        try:
            page_number = int(request.GET.get('page', 1))
            per_page = int(request.GET.get('per_page', 10))
        except ValueError:
            return JsonResponse({"error": "Invalid pagination parameters."}, status=400)

        # Query for similar profiles, excluding the current user
        queryset = Person.objects.filter(
            sexual_orientation=sexual_orientation
        ).exclude(id=current_user.id)

        # Apply pagination
        paginator = Paginator(queryset, per_page)
        try:
            paginated_profiles = paginator.get_page(page_number)
        except PageNotAnInteger:
            return JsonResponse({"error": "Page number is not an integer."}, status=400)
        except EmptyPage:
            return JsonResponse({"error": "Page out of range."}, status=404)

        # Prepare the response data with profile images
        profiles_data = []
        for person in paginated_profiles:
            try:
                profile = Profile.objects.get(person=person)
                profile_image = profile.profile_picture.url if profile.profile_picture else None
            except Profile.DoesNotExist:
                profile_image = None

            profiles_data.append({
                "username": person.username,
                "name": person.name,
                "relationship_status": person.relationship_status,
                "sexual_orientation": person.sexual_orientation,
                "race": person.race,
                "phone_number": person.phone_number,
                "social_media_api": person.social_media_api,
                "birth_date": person.birth_date,
                "email": person.email,
                "profile_image": profile_image,
            })

        # Prepare the response data
        response_data = {
            "current_page": paginated_profiles.number,
            "total_pages": paginated_profiles.paginator.num_pages,
            "total_profiles": paginated_profiles.paginator.count,
            "profiles": profiles_data,
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        # Log the error for debugging (you can configure Django logging)
        return JsonResponse({"error": "An unexpected error occurred.", "details": str(e)}, status=500)

