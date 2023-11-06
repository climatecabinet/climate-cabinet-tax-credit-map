"""Base settings used throughout the Django project.
"""

import os
from distutils.util import strtobool
from pathlib import Path

from configurations import Configuration


class BaseConfig(Configuration):
    """Defines configuration settings common across environments."""

    # File paths
    BASE_DIR = Path(__file__).parents[3]
    PROJECT_DIR = BASE_DIR / "pipeline"
    CONFIG_FILE = PROJECT_DIR / "pipeline.yml"
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # TODO: I (Todd) moved this here from production.py — is this ok?
    # Google Cloud Storage
    CLOUD_STORAGE_BUCKET = os.getenv("CLOUD_STORAGE_BUCKET", "")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", ""
    )

    LOAD_BATCH_SIZE = 1_000

    # DATA FILES
    GEOGRAPHY_TYPE_FILE = "geography_type.csv"
    PROGRAM_FILE = "program.csv"
    CENSUS_TRACT_FILE = "census_tract_pop.geoparquet"
    CENSUS_BLOCK_FILE = "CenPop2020_Mean_BG.txt"

    GEOGRAPHY_TYPE_PROGRAM_FILE = "geography_type_program.csv"
    STATE_GEOGRAPHY_FILE = "state_clean.geoparquet"
    COUNTY_GEOGRAPHY_FILE = "county_clean.geoparquet"
    DCI_GEOGRAPHY_FILE = "dci_clean.geoparquet"
    FOSSIL_FUEL_GEOGRAPHY_FILE = "ffe.geoparquet"
    COAL_GEOGRAPHY_FILE = "coal_closure.geoparquet"
    J40_GEOGRAPHY_FILE = "justice40.geoparquet"
    LOW_INCOME_GEOGRAPHY_FILE = "low_income_tracts_filtered.geoparquet"
    MUNICIPAL_UTIL_GEOGRAPHY_FILE = "municipal_utils.geoparquet"
    RURAL_COOP_GEOGRAPHY_FILE = "rural_coops.geoparquet"

    READ_CHUNK_SIZE = 1_000
    SMALL_CHUNK_SIZE = 100
    PQ_CHUNK_SIZE = 1_000

    # Installed apps
    INSTALLED_APPS = (
        # Default
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third party apps
        "corsheaders",
        # Your apps
        "tax_credit",
        "tests",
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    )

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    # General
    ADMINS = (("Author", ""),)
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True

    # URLs
    APPEND_SLASH = False
    ROOT_URLCONF = "config.urls"
    LOGIN_REDIRECT_URL = "/"

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "no"))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Templates
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("POSTGRES_DB", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "postgres"),
            "PORT": int(os.getenv("POSTGRES_PORT", 5432)),
            "CONN_MAX_AGE": int(os.getenv("POSTGRES_CONN_MAX_AGE", 0)),
            "DISABLE_SERVER_SIDE_CURSORS": False,
        }
    }

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["mail_admins", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {"handlers": ["console"], "level": "INFO"},
        },
    }
