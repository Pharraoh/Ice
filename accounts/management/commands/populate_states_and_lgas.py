import json
from django.core.management.base import BaseCommand
from accounts.models import State, LGA

class Command(BaseCommand):
    help = "Populates the database with states and LGAs from JSON file"

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        file_path = 'static/assets/json/nigeria-state-and-lgas.json'

        # Load the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Loop through the states and LGAs in the JSON
        for entry in data:
            state_name = entry['state']
            state_alias = entry['alias']
            lgas = entry['lgas']

            # Create or get the state
            state, created = State.objects.get_or_create(name=state_name)
            if created:
                self.stdout.write(f"State created: {state_name}")

            # Add LGAs for this state
            for lga_name in lgas:
                lga, lga_created = LGA.objects.get_or_create(name=lga_name, state=state)
                if lga_created:
                    self.stdout.write(f"  LGA created: {lga_name}")

        self.stdout.write("Database population complete!")
