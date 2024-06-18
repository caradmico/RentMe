import os
import django
import csv

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houseme_project.settings')
django.setup()

from houseme_app.models import Listing

def load_data(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Listing.objects.create(
                address_id=row['AddressID'],
                street=row['street'],
                city=row['city'],
                state=row['state'],
                zip_code=row['zip'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone=row['phone'],
                email=row['email'],
                bedroom=row['bedroom'],
                squarefootage=row['squarefootage'],
                price=row['price']
            )

if __name__ == "__main__":
    # Path to your CSV file
    csv_file_path = r'c:\Users\boobs\Projects\HouseMe\houseme_project\input.csv'
    load_data(csv_file_path)
    print(f"Data loaded from {csv_file_path}")
