from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

# Create the first user
username1 = fake.user_name()
password1 = 'password123'  # You can set a plain text password here
email1 = fake.email()
user1 = User.objects.create_user(username=username1, password=password1, email=email1)
user1.save()

# Create the second user
username2 = fake.user_name()
password2 = 'password456'  # Another plain text password
email2 = fake.email()
user2 = User.objects.create_user(username=username2, password=password2, email=email2)
user2.save()

# Print out user details for verification
print(f"Created user: {user1.username}, Password: {password1}, Email: {user1.email}")
print(f"Created user: {user2.username}, Password: {password2}, Email: {user2.email}")
