from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
import csv
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import Applicant, People, Property, PropertyImage, Rating, Application, Favorite, Profile

class ApplicantAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'is_approved', 'phone', 'desired_rent', 'move_in_date', 'lease_duration')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'is_approved', 'phone', 'desired_rent', 'move_in_date', 'lease_duration')}),
    )
    list_display = ('username', 'email', 'user_type', 'is_approved')
    search_fields = ('username', 'email')
    list_filter = ('is_approved', 'user_type')
    actions = ['delete_selected', 'import_users_csv']

    def import_users_csv(self, request, queryset):
        if 'apply' in request.POST:
            csv_file = request.FILES['csv_file']
            csv_reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in csv_reader:
                user = Applicant.objects.create_user(
                    username=row['username'],
                    email=row['email'],
                    password='default_password'
                )
                user.user_type = row['user_type']
                user.save()
                token = get_random_string()
                Profile.objects.create(user=user, reset_password_token=token)
                reset_url = f"{request.scheme}://{request.get_host()}/reset_password/{token}/"
                send_mail(
                    'Reset your password',
                    f'Please reset your password using the following link: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
            self.message_user(request, _("Users imported successfully"))
            return HttpResponse("Users imported successfully")
        
        form = '''
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="csv_file" accept=".csv">
                <input type="submit" name="apply" value="Upload">
            </form>
        '''
        return HttpResponse(form)

    import_users_csv.short_description = _("Import users from CSV")

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Number of extra forms to display

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('street1', 'city', 'state', 'rent_price')
    search_fields = ('street1', 'city', 'state')
    list_filter = ('state', 'city')

admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(People)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
admin.site.register(Rating)
admin.site.register(Application)
admin.site.register(Favorite)
admin.site.register(Profile)
