import json
from django.core.management.base import BaseCommand
from accounts.models import State, LGA

class Command(BaseCommand):
    help = "Populates the database with states and LGAs from JSON file"

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        file_path = 'static/assets/json/pop.json'

        # Load the JSON data
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("JSON file not found. Please check the file path."))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON format: {e}"))
            return

        # Loop through the states and LGAs in the JSON
        for entry in data:
            state_name = entry['state']  # Use the "state" key
            lgas = entry['lgas']  # Use the "lgas" key

            # Create or get the state
            state, created = State.objects.get_or_create(name=state_name)
            if created:
                self.stdout.write(f"State created: {state_name}")

            # Add LGAs for this state
            for lga_entry in lgas:
                lga_name = lga_entry['name']  # Get the LGA name from the nested structure
                lga, lga_created = LGA.objects.get_or_create(name=lga_name, state=state)
                if lga_created:
                    self.stdout.write(f"  LGA created: {lga_name}")

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
