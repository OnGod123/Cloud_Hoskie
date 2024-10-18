from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person
from .emails import send_welcome_email
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("welcome to the Home page")

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse('Invalid request method.')

def submit(request):
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
