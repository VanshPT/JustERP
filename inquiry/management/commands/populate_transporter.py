# import_transporters.py

from django.core.management.base import BaseCommand
import pandas as pd
from inquiry.models import Transporter, TruckDetails

class Command(BaseCommand):
    help = 'Import transporters and map vehicles from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.stdout.write(f'Importing data from {file_path}')

        try:
            df = pd.read_excel(file_path)
            data = df.to_dict(orient='records')

            for row in data:
                transporter_name = row['Group Name']
                truck_number = row['Vehicle']

                transporter, _ = Transporter.objects.get_or_create(transporter_name=transporter_name)
                truck_details, _ = TruckDetails.objects.get_or_create(truck_number=truck_number)

                transporter.truck_details.add(truck_details)

            self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
