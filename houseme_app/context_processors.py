from django.conf import settings


def public_config(request):
    """Expose non-secret frontend config. Mapbox pk.* tokens are public client tokens."""
    return {
        'MAPBOX_ACCESS_TOKEN': getattr(settings, 'MAPBOX_ACCESS_TOKEN', ''),
    }
