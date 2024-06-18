from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # Default login
    path('login/<str:user_type>/', views.login, name='login_with_type'),  # Login with user_type
    path('logout/', views.logout, name='logout'),
    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('renter_dashboard/', views.renter_dashboard, name='renter_dashboard'),
    path('admin/', views.admin, name='admin'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('property/portfolio/', views.property_portfolio, name='property_portfolio'),
    path('add_property/', views.add_property, name='add_property'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('login_redirect/<str:user_type>/', views.login_redirect, name='login_redirect'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('apply/owner/', views.owner_apply, name='owner_apply'),
    path('apply/renter/', views.renter_apply, name='renter_apply'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin/approve/<int:application_id>/', views.approve_application, name='approve_application'),  # Approve application
    path('admin/reject/<int:application_id>/', views.reject_application, name='reject_application'),  # Reject application
    path('listings/', views.listings, name='listings'),

]
