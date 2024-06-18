# houseme_project/urls.py
from django.contrib import admin
from django.urls import path, include  # Include the include function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('houseme_app.urls')),  # Include the URLs from houseme_app
]
