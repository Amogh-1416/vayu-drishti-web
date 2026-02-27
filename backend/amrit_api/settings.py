"""
Django settings for amrit_api project.
Updated for macOS (PostGIS + Redis + WebSockets)
"""

import os
import platform
from pathlib import Path
from dotenv import load_dotenv

# --- PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file we created
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

# --- GEOSPATIAL LIBRARY CONFIGURATION ---
# This resolves the ImproperlyConfigured error on your MacBook Air
if platform.system() == 'Darwin':
    GDAL_LIBRARY_PATH = '/opt/homebrew/lib/libgdal.dylib'
    GEOS_LIBRARY_PATH = '/opt/homebrew/lib/libgeos_c.dylib'
elif os.name == 'nt':
    GDAL_LIBRARY_PATH = r'C:/Program Files/PostgreSQL/17/bin/libgdal-35.dll'
    GEOS_LIBRARY_PATH = r'C:/Program Files/PostgreSQL/17/bin/libgeos_c.dll'

# --- SECURITY ---
SECRET_KEY = "django-insecure-65kg(kwvqw6qja2l5f!y)_14!c#8xr*@ov#c53vi=e&$!7r^1f"
DEBUG = True
# Allows the backend to accept connections from local network/IPs
ALLOWED_HOSTS = ['*']

# Required for WebSockets to remain open; prevents browser auto-close
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    "daphne",  # Must be at the top for ASGI
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",  # Required for PostGIS
    "rest_framework",
    "rest_framework_gis",
    "channels",  # Required for Real-Time Telemetry
    "corsheaders",
    'core',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", # Must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "amrit_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "amrit_api.wsgi.application"
ASGI_APPLICATION = "amrit_api.asgi.application" # Points to asgi.py

# --- DATABASE (PostgreSQL + PostGIS) ---
# Pulled from your .env file created earlier
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get('DB_NAME', 'vayu_drishti'),
        "USER": os.environ.get('DB_USER', 'saisaatvikbetanabhotla'),
        "PASSWORD": os.environ.get('DB_PASSWORD', ''),
        "HOST": os.environ.get('DB_HOST', '127.0.0.1'),
        "PORT": os.environ.get('DB_PORT', 5432),
    }
}

# --- CHANNELS / REDIS ---
# Using native Redis via Homebrew
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# --- CORS CONFIGURATION ---
CORS_ALLOW_ALL_ORIGINS = True

# --- STANDARD SETTINGS ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"