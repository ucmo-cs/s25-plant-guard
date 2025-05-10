from django.core.management.base import BaseCommand
from sensors.services import fetch_and_store_pi_data

class Command(BaseCommand):
    help = "Fetches Pi sensor data and stores it"

    def handle(self, *args, **kwargs):
        success = fetch_and_store_pi_data()
        if success:
            self.stdout.write(self.style.SUCCESS("Successfully fetched and saved Pi data."))
        else:
            self.stderr.write(self.style.ERROR("Failed to fetch or save Pi data."))
