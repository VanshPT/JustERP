import pandas as pd
from django.core.management.base import BaseCommand
from inquiry.models import TruckDetails, TruckCapacity, TruckLength, TruckType

class Command(BaseCommand):
    help = 'Populate TruckDetails model from dataset'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_path', type=str, help='Path to the XLSX file containing the dataset')

    def handle(self, *args, **kwargs):
        xlsx_path = kwargs['xlsx_path']

        # Load dataset from XLSX file
        df = pd.read_excel(xlsx_path)

        # Iterate through each row in the dataset
        for index, row in df.iterrows():
            truck_number = row['Vehicle']
            ageing_duration = row['Ageing Duration']

            # Check if a truck with the same truck_number already exists
            if not TruckDetails.objects.filter(truck_number=truck_number).exists():
                # Get the next truck capacity value in the cycle
                next_truck_capacity = self.get_next_truck_capacity(index)

                # Create TruckDetails object with the corresponding values
                truck_details = TruckDetails.objects.create(
                    truck_number=truck_number,
                    truck_type=TruckType.objects.get(tt_id=1),  # Assuming tt_id=1 is for "Cement Truck"
                    truck_capacity=TruckCapacity.objects.get(truck_capacity=next_truck_capacity),
                    truck_length=TruckLength.objects.get(truck_length="22 feet"),
                    ageing_duration=ageing_duration
                )

                # Print confirmation message
                self.stdout.write(self.style.SUCCESS(f"TruckDetails created: {truck_details}"))

    def get_next_truck_capacity(self, index):
        # List of truck capacity values in the desired order
        truck_capacities = ["6 ton", "2 ton", "10 ton", "1.5 ton", "32 ton", "7 ton", "12 ton", "6 ton", "2 ton", "18 ton", "4.5 ton"]
        # Get the index of the truck capacity in the cycle
        cycle_index = index % len(truck_capacities)
        # Return the truck capacity at the cycle index
        return truck_capacities[cycle_index]
