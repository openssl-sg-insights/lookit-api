"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

MODE = "prod"  # Overridden by local settings.
ENVIRONMENT = os.environ.get("ENVIRONMENT", "develop")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# root path for ember builds
EMBER_BUILD_ROOT_PATH = os.path.join(BASE_DIR, "../ember_build")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "c*si4oji5r=#)5+6e$bi@an%v)(n2be2+1(s985uh4mu3jq!qt"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", False))
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(" ") if h]

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 24  # One day in seconds

AUTH_USER_MODEL = "accounts.User"
GUARDIAN_MONKEY_PATCH = False

# S3 Bucket name where video attachments are stored
BUCKET_NAME = os.environ.get("BUCKET_NAME", "fakeBucketName")
# Pipe webhook key for authentication
PIPE_WEBHOOK_KEY = os.environ.get("PIPE_WEBHOOK_KEY", "abcdefghijkl1")

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    # third-party
    "django_extensions",
    "guardian",
    "localflavor",
    "rest_framework",
    "bootstrap3",
    "ace_overlay",
    "corsheaders",
    "rest_framework.authtoken",
    "rest_framework_json_api",
    "storages",
    "django_celery_beat",
    # our stuff
    "api",
    "web",
    "accounts",
    "studies",
    "exp",
    # at the bottom so overriding form widget templates have a fallback -
    # See https://stackoverflow.com/a/46836189
    "django.forms",
    # "django.contrib.admin",
    "project.apps.TwoFactorAuthProtectedAdminConfig",
    # "allauth.socialaccount",
    # "allauth.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar", "shells", "sslserver"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "pyinstrument.middleware.ProfilerMiddleware",
    ]
else:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        environment=os.environ.get("ENVIRONMENT"),
        dsn=os.environ.get("SENTRY_DSN", None),
        release=os.environ.get("GIT_COMMIT", "No version"),
        integrations=[DjangoIntegration(), CeleryIntegration()],
    )


INTERNAL_IPS = ["127.0.0.1"]

AUTHENTICATION_BACKENDS = (
    "accounts.backends.TwoFactorAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",  # this is default
    "guardian.backends.ObjectPermissionBackend",
    # "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = "project.urls"
LOGIN_URL = "/login/"
EXPERIMENTER_LOGIN_URL = "/accounts/login/"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["django/forms/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.db.backends.postgresql",  # django.db.backends.postgresql
        "NAME": os.environ.get("DB_NAME", "lookit"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
# Why 16 characters?
# See https://www.lmgsecurity.com/how-long-should-your-password-be-a-technical-guide-to-a-safe-password-length-policy/
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 16},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "api.pagination.PageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "api.parsers.JSONAPIParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "api.renderers.JsonApiWithUuidRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "SEARCH_PARAM": "filter[search]",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

JSON_API_PLURALIZE_TYPES = True

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost:8000")
SITE_NAME = os.environ.get("SITE_NAME", "Lookit")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# base url for experiments, should be GCS bucket in prod
EXPERIMENT_BASE_URL = os.environ.get("EXPERIMENT_BASE_URL")

BASE_URL = os.environ.get(
    "BASE_URL", "https://localhost:8000"
)  # default to ember base url

LOGIN_REDIRECT_URL = "web:home"
ACCOUNT_LOGOUT_REDIRECT_URL = os.environ.get("ACCOUNT_LOGOUT_REDIRECT_URL", "/api/")
LOGOUT_REDIRECT_URL = "web:home"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"


# Configuration for cross-site requests
CORS_ORIGIN_ALLOW_ALL = bool(os.environ.get("CORS_ORIGIN_ALLOW_ALL", True))
CORS_ORIGIN_WHITELIST = [
    h for h in os.environ.get("CORS_ORIGIN_WHITELIST", "").split(" ") if h
]

if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    # if we're trying to use cloud storage
    STATICFILES_LOCATION = "static"
    STATICFILES_STORAGE = "project.storages.LookitStaticStorage"
    STATIC_URL = os.environ.get("STATIC_URL", "/static/")

    MEDIAFILES_LOCATION = "media"
    DEFAULT_FILE_STORAGE = "project.storages.LookitMediaStorage"
    MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

    EXPERIMENT_LOCATION = "experiments"

    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME", "")
    GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID", "")

    GS_PRIVATE_BUCKET_NAME = os.environ.get("GS_PRIVATE_BUCKET_NAME", "")
else:
    # we know nothing about cloud storage
    print(
        "-------------------Why yes, we are using local assets!-------------------------"
    )
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"

    STATICFILES_LOCATION = "/static"

    MEDIAFILES_LOCATION = "/media"

    EXPERIMENT_LOCATION = "/experiments"

    GS_BUCKET_NAME = None
    GS_PROJECT_ID = None

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "_static"),)

EMAIL_FROM_ADDRESS = os.environ.get("EMAIL_FROM_ADDRESS", "lookit.robot@some.domain")
DEFAULT_FROM_EMAIL = EMAIL_FROM_ADDRESS  # for Django-generated password reset emails

EMAIL_BACKEND = (
    "sgbackend.SendGridBackend"
    if not DEBUG
    else "django.core.mail.backends.console.EmailBackend"
)
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "M31tSt331B34m5")

# United States will show up first in the countries list on the Demographic Data form
COUNTRIES_FIRST = ["US"]

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
EMBER_EXP_PLAYER_REPO = os.environ.get(
    "EMBER_EXP_PLAYER_REPO", "https://github.com/lookit/ember-lookit-frameplayer"
)
EMBER_EXP_PLAYER_BRANCH = os.environ.get("EMBER_EXP_PLAYER_BRANCH", "master")
EMBER_ADDONS_REPO = os.environ.get(
    "EMBER_ADDONS_REPO", "https://github.com/lookit/exp-addons"
)  # leave for compatibility with previous migrations
EMBER_ADDONS_BRANCH = os.environ.get("EMBER_ADDONS_BRANCH", "master")

RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "guest")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")
RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "/")

CELERY_BROKER_URL = os.environ.get(
    "BROKER_URL",
    f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}",
)
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_ROUTES = {
    "studies.tasks.ember_build_and_gcp_deploy": {"queue": "builds"},
    "studies.tasks.build_zipfile_of_videos": {"queue": "builds"},
    "studies.tasks.build_framedata_dict": {"queue": "builds"},
    "studies.tasks.delete_video_from_cloud": {"queue": "cleanup"},
    "studies.tasks.cleanup*": {"queue": "cleanup"},
    "studies.helpers.send_mail": {"queue": "email"},
}
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = ( os.path.join(SITE_ROOT, 'locale'), )
