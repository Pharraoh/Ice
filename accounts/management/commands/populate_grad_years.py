# accounts/management/commands/populate_grad_years.py
import json
from django.core.management.base import BaseCommand
from accounts.models import GradYear

class Command(BaseCommand):
    help = "Populates the database with Grad Years from a JSON file"

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        file_path = 'static/assets/json/grad_years.json'  # Adjust path as needed

        # Load the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Loop through the JSON data and create GradYear objects
        for entry in data:
            year = entry['year']
            GradYear.objects.get_or_create(year=year)  # Ensure unique grad years
            self.stdout.write(f"Grad Year {year} created.")

        self.stdout.write("Grad Year data population complete!")
