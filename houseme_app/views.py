from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistrationForm, LoginForm, PropertyForm, ApplicantForm, RenterForm
from .models import Applicant, People, Property, Application, Favorite, Profile
from .decorators import approved_renter_or_admin_required
import random
from .forms import DocumentForm
from .models import Document
from django.core.files.storage import FileSystemStorage

def index(request):
    # Fetch approved applications with their associated properties
    approved_applications = list(Application.objects.filter(status='approved').select_related('property').order_by('-property__available_date'))

    # Ensure at least 12 properties, repeating if necessary
    total_properties = len(approved_applications)
    min_properties = 12
    if total_properties < min_properties:
        multiplier = (min_properties // total_properties) + 1
        approved_applications = approved_applications * multiplier
    
    # Shuffle the list to get a random assortment
    random.shuffle(approved_applications)
    approved_applications = approved_applications[:min_properties]  # Ensure only 12 items

    return render(request, 'index.html', {'approved_applications': approved_applications})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data.get('password1'))
            user.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect_user_dashboard(user.user_type)
        else:
            messages.error(request, form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request, user_type=None):
    next_url = request.GET.get('next', reverse('index'))
    if request.user.is_authenticated:
        return redirect(next_url)  # Redirect to original destination if already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    auth_login(request, user)
                    messages.success(request, 'Admin login successful.')
                    return redirect(next_url if next_url else '/admin/')  # Redirect to Django admin panel
                elif user_type and user.user_type != user_type:
                    messages.error(request, f"You are not registered as {user_type.capitalize()}. Redirected to your dashboard.")
                    return redirect_user_dashboard(user.user_type)  # Redirect to correct dashboard
                else:
                    auth_login(request, user)
                    # Redirect to original destination or default dashboard
                    redirect_to = next_url if next_url else redirect_user_dashboard(user.user_type)
                    return redirect(redirect_to)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'user_type': user_type, 'next': next_url})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def owner_dashboard(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'You are not authorized to access the owner dashboard.')
        return redirect('index')
    properties = Property.objects.filter(owner=request.user.id)
    return render(request, 'owner_dashboard.html', {'properties': properties})

@login_required
def renter_dashboard(request):
    if request.user.user_type != 'renter':
        messages.error(request, 'You are not authorized to access the renter dashboard.')
        return redirect('index')

    applications = Application.objects.filter(applicant=request.user)
    favorites = Favorite.objects.filter(applicant=request.user)
    return render(request, 'renter_dashboard.html', {'applications': applications, 'favorites': favorites})

def admin_login(request):
    next_url = request.GET.get('next', '/admin/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                auth_login(request, user)
                messages.success(request, 'Admin login successful.')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password or not an admin.')
        else:
            messages.error(request, form.errors)
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form, 'next': next_url})

def admin(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You must be logged in as an admin to view this page.')
        return redirect('admin_login')
    return redirect('/admin/')

def login_redirect(request, user_type):
    next_url = request.GET.get('next', reverse('index'))
    if request.user.is_authenticated:
        return redirect_user_dashboard(request.user.user_type)
    else:
        login_url = reverse('login_with_type', kwargs={'user_type': user_type}) + f'?next={next_url}'
        return redirect(login_url)

def redirect_user_dashboard(user_type):
    if user_type == 'owner':
        return redirect('owner_dashboard')
    elif user_type == 'renter':
        return redirect('renter_dashboard')
    elif user_type == 'admin':
        return redirect('/admin/')  # Redirect to the default Django admin panel
    else:
        return redirect('index')

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('property_portfolio')
        else:
            messages.error(request, form.errors)
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})

@login_required
def property_portfolio(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'property_portfolio.html', {'properties': properties})

@login_required
def owner_apply(request):
    if request.user.user_type != 'owner':
        return redirect('index')
    
    if request.method == 'POST':
        print("Owner application form submitted")
        form = PropertyForm(request.POST)
        if form.is_valid():
            print("Owner application form is valid")
            property = form.save(commit=False)
            property.owner = request.user
            property.save()

            # Create a new application
            Application.objects.create(applicant=request.user, property=property, status='pending')

            return redirect('owner_dashboard')
        else:
            print("Owner application form is invalid")
            print(form.errors)
    else:
        form = PropertyForm()
    return render(request, 'owner_apply.html', {'form': form})

@login_required
def renter_apply(request):
    if request.user.user_type != 'renter':
        return redirect('index')
    
    if request.method == 'POST':
        print("Renter application form submitted")
        form = RenterForm(request.POST)
        if form.is_valid():
            print("Renter application form is valid")
            form.save()

            # Create a new application
            Application.objects.create(applicant=request.user, status='pending')

            return redirect('renter_dashboard')
        else:
            print("Renter application form is invalid")
            print(form.errors)
    else:
        form = RenterForm()
    return render(request, 'renter_apply.html', {'form': form})

def reset_password(request, token):
    try:
        profile = Profile.objects.get(reset_password_token=token)
    except Profile.DoesNotExist:
        return HttpResponse("Invalid token")

    if request.method == 'POST':
        form = SetPasswordForm(profile.user, request.POST)
        if form.is_valid():
            form.save()
            profile.reset_password_token = None
            profile.save()
            auth_login(request, profile.user)
            return redirect('some_dashboard_view')  # Redirect to some dashboard or home page
    else:
        form = SetPasswordForm(profile.user)
    return render(request, 'reset_password.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Check if email matches an existing user
        try:
            user_profile = Profile.objects.get(user__email=email)
            messages.success(request, f'Message from {name} linked to user: {user_profile.user.username}')
        except Profile.DoesNotExist:
            messages.success(request, 'Message sent successfully!')

        # Here you can add logic to save the message or send an email
        # For now, we'll just print it to the console
        print(f'Name: {name}, Email: {email}, Phone: {phone}, Message: {message}')
        
        return redirect('contact')

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    applications = Application.objects.filter(status='pending')
    return render(request, 'admin_dashboard.html', {'applications': applications})

@user_passes_test(lambda u: u.is_staff)
def approve_application(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
        application.status = 'approved'
        application.save()
        messages.success(request, 'Application approved successfully.')
    except Application.DoesNotExist:
        messages.error(request, 'Application does not exist.')
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_staff)
def reject_application(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
        application.status = 'rejected'
        application.save()
        messages.success(request, 'Application rejected successfully.')
    except Application.DoesNotExist:
        messages.error(request, 'Application does not exist.')
    return redirect('admin_dashboard')

@approved_renter_or_admin_required
def listings(request):
    # Fetch approved applications with their associated properties
    approved_applications = Application.objects.filter(status='approved').select_related('property').order_by('-property__available_date')

    # Debug print to check what we are fetching
    for application in approved_applications:
        print(f"Property: {application.property.city}, {application.property.description}, Rent: {application.property.rent_price}, Status: {application.status}")

    return render(request, 'listings.html', {'approved_applications': approved_applications})

def home(request):
    approved_applications = Application.objects.filter(status='approved').select_related('property').order_by('-property__available_date')[:12]
    return render(request, 'index.html', {'approved_applications': approved_applications})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

def upload_document(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('sign_document', file_name=uploaded_file.name)
    return render(request, 'upload_document.html')
