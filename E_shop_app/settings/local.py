from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    # }
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add DB name or path to db file if using sqlite3.
        'NAME': config.POSTGRES_DB,
        'USER': config.POSTGRES_USER,
        'PASSWORD': config.POSTGRES_PASSWORD,
        'HOST': config.POSTGRES_HOST,
        'PORT': config.POSTGRES_PORT,
    },
}
