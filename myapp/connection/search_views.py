from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
import uuid
from myapp.models import Person 
from .models import ConnectionLogic
from myapp.profile.model_profile import Profile

def search_view(request):
    person = Person.objects.get(user=request.user)
    if not check_valid_payment_for_person(person):
        return render(request, 'payment_required.html', {'message': 'Please make a payment to enjoy the service.'})

    criteria = {
        'race': request.GET.get('race'),
        'sexual_orientation': request.GET.get('sexual_orientation'),
        'min_age': request.GET.get('min_age'),
        'max_age': request.GET.get('max_age'),
        'skin_color': request.GET.get('skin_color'),
        'min_weight': request.GET.get('min_weight'),
        'max_weight': request.GET.get('max_weight'),
        'min_height': request.GET.get('min_height'),
        'max_height': request.GET.get('max_height'),
    }
    min_birth_date, max_birth_date = calculate_age_range(criteria['min_age'], criteria['max_age'])
    criteria['min_age'] = min_birth_date
    criteria['max_age'] = max_birth_date

    # Perform non-strict search
    results = search_persons(criteria)
    profiles = [{'id': result.id, 'username': result.username, 'name': result.name} for result in results]

    return render(request, 'search_results.html', {'results': profiles})
def send_connection_request(request, to_user_id):
    """
    Handle sending connection requests.
    """
    # Get the sender (from_user) and the recipient (to_user)
    from_user = Person.objects.get(user=request.user)
    to_user = get_object_or_404(Person, id=to_user_id)

    # Create connection request
    connection = ConnectionLogic.objects.create(
        from_user=from_user,
        to_user=to_user
    )

    # Get the sender's profile
    from_user_profile = Profile.objects.get(person=from_user)

    # Prepare the profile data to send to the frontend
    profile_data = {
        'id': str(from_user_profile.id),
        'username': from_user_profile.username,
        'bio': from_user_profile.bio,
        'social_media_url': from_user_profile.social_media_url,
        'user_video': from_user_profile.user_video,
        'profile_picture': from_user_profile.profile_picture.url if from_user_profile.profile_picture else None,
    }

    # Return JSON response with connection info and from_user profile
    return JsonResponse({
        'message': 'Connection request sent successfully!',
        'connection_id': str(connection.id),
        'from_user_profile': profile_data
    })
