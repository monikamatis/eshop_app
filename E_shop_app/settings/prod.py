from .base import *

# Setting DEBUG to False as necessary ib any production environment

DEBUG = False


# Since DEBUG is set to False, all exceptions will be sent to provided ADMIN emails

ADMINS = [
    ('Monika Matis', 'monika@marysia.app'),
]


# For security reasons only hosts included in the list below will be able to serve the project.
# The list is to be restricted later, for now it includes all hosts

ALLOWED_HOSTS = ['*']


# Production database settings are here

DATABASES = {
    'default': {

    }
}
