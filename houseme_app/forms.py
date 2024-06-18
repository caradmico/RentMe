# houseme_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Applicant, Property, Document

class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Applicant.USER_TYPE_CHOICES)
    
    class Meta:
        model = Applicant
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'street1', 'street2', 'city', 'state', 'zip', 'description', 'bedrooms', 'square_footage', 
            'rent_price', 'deposit_price', 'pets_allowed', 'pets_deposit', 'ada_accessible', 
            'available_date', 'lease_terms', 'manager_name', 'manager_phone', 'manager_email'
        ]

        widgets = {
            'available_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicantForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Applicant.USER_TYPE_CHOICES)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    # Property fields
    street1 = forms.CharField(max_length=100)
    street2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip = forms.CharField(max_length=10)
    description = forms.CharField(widget=forms.Textarea, required=False)
    bedrooms = forms.IntegerField()
    square_footage = forms.IntegerField()
    rent_price = forms.DecimalField(max_digits=10, decimal_places=2)
    deposit_price = forms.DecimalField(max_digits=10, decimal_places=2)
    pets_allowed = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    pets_deposit = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    ada_accessible = forms.BooleanField(required=False)
    available_date = forms.DateField(widget=forms.SelectDateWidget)
    lease_terms = forms.CharField(max_length=50)
    manager_name = forms.CharField(max_length=100)
    manager_phone = forms.CharField(max_length=50)
    manager_email = forms.EmailField()

    class Meta:
        model = Applicant
        fields = ['username', 'password1', 'password2', 'user_type', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            Property.objects.create(
                owner=user,
                street1=self.cleaned_data['street1'],
                street2=self.cleaned_data['street2'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zip=self.cleaned_data['zip'],
                description=self.cleaned_data['description'],
                bedrooms=self.cleaned_data['bedrooms'],
                square_footage=self.cleaned_data['square_footage'],
                rent_price=self.cleaned_data['rent_price'],
                deposit_price=self.cleaned_data['deposit_price'],
                pets_allowed=self.cleaned_data['pets_allowed'],
                pets_deposit=self.cleaned_data.get('pets_deposit'),
                ada_accessible=self.cleaned_data['ada_accessible'],
                available_date=self.cleaned_data['available_date'],
                lease_terms=self.cleaned_data['lease_terms'],
                manager_name=self.cleaned_data['manager_name'],
                manager_phone=self.cleaned_data['manager_phone'],
                manager_email=self.cleaned_data['manager_email']
            )
        return user

class RenterForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'desired_rent', 'move_in_date', 'lease_duration'
        ]

        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']