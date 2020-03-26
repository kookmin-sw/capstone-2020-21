from .base import *

# Local default : uses db.sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(Path(BASE_DIR, 'db.sqlite3')),
    }
}

AUTH_PASSWORD_VALIDATORS = []