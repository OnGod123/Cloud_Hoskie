from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create fake users for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count'] or 10  # Default to creating 10 users if no count is provided
        fake = Faker()

        for _ in range(count):
            username = fake.user_name()
            email = fake.email()
            password = 'password123'  # or use a more complex one

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(self.style.SUCCESS(f'Created user {username}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} fake users.'))
