from pathlib import Path
import os
import environ

# Initialize environment variables
env = environ.Env()
# Read the .env file
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Debug statements to print loaded environment variables
print("DB_NAME:", env('DB_NAME', default=None))
print("DB_USER:", env('DB_USER', default=None))
print("DB_PASSWORD:", env('DB_PASSWORD', default=None))
print("DB_HOST:", env('DB_HOST', default=None))
print("DB_PORT:", env.int('DB_PORT', default=None))

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = str(BASE_DIR / 'staticfiles')

print("BASE_DIR is set to:", BASE_DIR)
print("STATIC_ROOT is set to:", STATIC_ROOT)

SECRET_KEY = env('SECRET_KEY', default='your-secret-key-here')
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'houseme_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env.int('DB_PORT'),  # Ensures this is an integer
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'houseme_app.Applicant'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

print("Final STATIC_ROOT is set to:", STATIC_ROOT)
print("STATICFILES_DIRS is set to:", STATICFILES_DIRS)
print("STATIC_ROOT exists:", os.path.exists(STATIC_ROOT))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
    print("STATIC_ROOT created:", os.path.exists(STATIC_ROOT))
