from django.core.management.base import BaseCommand
from myapp.models import Person  # This is your existing model in the SQL database
from pymongo import MongoClient  # Importing pymongo to work directly with MongoDB

class Command(BaseCommand):
    help = 'Migrate data from SQL database to MongoDB'

    def handle(self, *args, **kwargs):
        # Step 1: Get all the records from your existing SQL database
        old_people = Person.objects.all()

        # Step 2: Set up a MongoDB connection using pymongo
        client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
        db = client['mydatabase']  # Use the MongoDB database name you want
        collection = db['person']  # The collection where you will store the data

        # Step 3: Iterate through all old records and save them to MongoDB
        for old_person in old_people:
            new_person_data = {
                'username': old_person.username,
                'name': old_person.name,
                'relationship_status': old_person.relationship_status,
                'sexual_orientation': old_person.sexual_orientation,
                'race': old_person.race,
                'phone_number': old_person.phone_number,
                'social_media_api': old_person.social_media_api,
                'birth_date': old_person.birth_date,
                'email': old_person.email,
                'password': old_person.password,  # Ensure this is hashed if needed
            }

            # Step 4: Insert the new data into the MongoDB collection
            collection.insert_one(new_person_data)

        self.stdout.write(self.style.SUCCESS('Data migration completed successfully'))
