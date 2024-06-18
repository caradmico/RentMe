import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from houseme_app.models import Property
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Import users and properties from a single CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        User = get_user_model()
        
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create or update user
                user, created = User.objects.get_or_create(
                    username=row['username'],
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                    }
                )
                if created:
                    user.set_password(row['password'])
                    user.save()
                    # Send email to new user
                    send_mail(
                        'Welcome to HouseMe',
                        f'Your account has been created with the username: {row["username"]}. '
                        f'Please log in and change your password. Your temporary password is: {row["password"]}',
                        'admin@houseme.com',
                        [user.email],
                        fail_silently=False,
                    )
                else:
                    self.stdout.write(f"User already exists: {user.username}")

                # Create or update property
                property, created = Property.objects.get_or_create(
                    owner=user,
                    street1=row['street1'],
                    defaults={
                        'street2': row['street2'],
                        'city': row['city'],
                        'state': row['state'],
                        'zip': row['zip'],
                        'description': row['description'],
                        'bedrooms': row['bedrooms'],
                        'square_footage': row['square_footage'],
                        'rent_price': row['rent_price'],
                        'deposit_price': row['deposit_price'],
                        'pets_allowed': row['pets_allowed'],
                        'pets_deposit': row['pets_deposit'],
                        'ada_accessible': row['ada_accessible'],
                        'available_date': row['available_date'],
                        'lease_terms': row['lease_terms'],
                        'manager_name': row['manager_name'],
                        'manager_phone': row['manager_phone'],
                        'manager_email': row['manager_email'],
                    }
                )
                self.stdout.write(f"Property {'created' if created else 'updated'}: {property.street1}")
