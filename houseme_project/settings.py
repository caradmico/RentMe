from pathlib import Path
import os
import environ
from django.core.exceptions import ImproperlyConfigured

# Initialize environment variables
env = environ.Env()
# Read the .env file when present (local). Render injects env vars directly.
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Placeholder values from .env.example — never valid when DEBUG is False.
PLACEHOLDER_SECRET_KEYS = frozenset({
    '',
    'change-me',
    'your-secret-key-here',
})


def require_production_secret(secret_key, debug):
    """Fail loud if a placeholder SECRET_KEY is used with DEBUG off."""
    if not debug and secret_key in PLACEHOLDER_SECRET_KEYS:
        raise ImproperlyConfigured(
            'SECRET_KEY must be set to a non-placeholder value when DEBUG is False.'
        )


SECRET_KEY = env('SECRET_KEY', default='change-me')
# Production-safe default: unset DEBUG means False. Set DEBUG=True in .env for local.
DEBUG = env.bool('DEBUG', default=False)
MAPBOX_ACCESS_TOKEN = env('MAPBOX_ACCESS_TOKEN', default='')

require_production_secret(SECRET_KEY, DEBUG)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Render sets RENDER_EXTERNAL_HOSTNAME to the public host (e.g. houseme.onrender.com).
# Append it so the first deploy works before you add a custom domain.
_render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '').strip()
if _render_hostname:
    if _render_hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_render_hostname)
    _render_origin = f'https://{_render_hostname}'
    if _render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_render_origin)

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'houseme_app',
    'crispy_forms',
    'crispy_bootstrap4',
    'sass_processor',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'houseme_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'houseme_app' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'houseme_app.context_processors.public_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'houseme_project.wsgi.application'

# Render Postgres exposes a private DATABASE_URL (connectionString), not DB_HOST.
# Local / Docker keep using discrete DB_* vars from .env.
if env('DATABASE_URL', default=''):
    DATABASES = {'default': env.db('DATABASE_URL')}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default='houseme_db'),
            'USER': env('DB_USER', default='houseme'),
            'PASSWORD': env('DB_PASSWORD', default=''),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env.int('DB_PORT', default=5432),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'houseme_app' / 'static',
]
# WhiteNoise serves files collected into STATIC_ROOT (see collectstatic in render.yaml).
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'houseme_app.Applicant'

# Contact form uses Django's email API. Default is the console backend
# (messages print to the process log, not a mailbox). Point EMAIL_BACKEND
# at SMTP only in the environment — no mail credentials are committed.
EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@localhost')
CONTACT_EMAIL = env('CONTACT_EMAIL', default='webmaster@localhost')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'houseme_app', 'static')
SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'node_modules'),
]
SASS_OUTPUT_STYLE = 'compressed'
COMPRESS_OFFLINE = True

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
