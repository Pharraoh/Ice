import json
from django.core.management.base import BaseCommand
from accounts.models import College

class Command(BaseCommand):
    help = "Populate the database with colleges from JSON file"

    def handle(self, *args, **kwargs):
        file_path = 'static/assets/json/colleges.json'

        with open(file_path, 'r') as file:
            data = json.load(file)

        for college_data in data:
            college_name = college_data['name']
            college, created = College.objects.get_or_create(name=college_name)
            if created:
                self.stdout.write(f"Created college: {college_name}")

        self.stdout.write("Database population complete!")
