from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from datetime import date
from django.conf import settings


class Applicant(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('renter', 'Renter'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, default='000-000-0000')
    desired_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    move_in_date = models.DateField(null=True, blank=True)
    lease_duration = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=False) 

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)


class Profile(models.Model):
    user = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reset_password_token = get_random_string(64)  # Specify the length here
        super().save(*args, **kwargs)


# Signal to create or update the Profile whenever a User is created or updated
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Applicant)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)


class People(models.Model):
    accountID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=50)  # Increased from 20 to 50
    email = models.EmailField(max_length=100)
    business_license_number = models.CharField(max_length=50, blank=True)
    registered_business_name = models.CharField(max_length=100, blank=True)
    class_type = models.CharField(max_length=50)
    join_date = models.DateField()
    account_status = models.CharField(max_length=50)


class Property(models.Model):
    owner = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    description = models.TextField(default='No description provided')
    bedrooms = models.IntegerField(default=1)
    square_footage = models.IntegerField(default=0)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deposit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    pets_allowed = models.CharField(max_length=50, default='No')
    pets_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ada_accessible = models.BooleanField(default=False)
    available_date = models.DateField(default=date.today)
    lease_terms = models.CharField(max_length=50, default='Month-to-Month')
    manager_name = models.CharField(max_length=100, default='Manager Name')
    manager_phone = models.CharField(max_length=50, default='000-000-0000')  # Increased from 20 to 50
    manager_email = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.street1


class Rating(models.Model):
    ratingID = models.AutoField(primary_key=True)
    accountID = models.ForeignKey(People, on_delete=models.CASCADE)
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')


class Favorite(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)


class Listing(models.Model):
    address_id = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)  # Increased from 20 to 50
    email = models.EmailField()
    bedroom = models.IntegerField()
    squarefootage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner}"

