from .base import *  # noqa

# Maps can be requested using <map_slug>.localhost.
ALLOWED_HOSTS = ['.localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'db',
        'PASSWORD': 'db',
        'HOST': 'db',
    }
}

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", "django_extensions")  # noqa

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer')

SECRET_KEY = 'd)1)w5(&@^a=avczu_j$y0a)!-zq%v_vfywfuzv8rq_51t)-^+'

SHELL_PLUS_POST_IMPORTS = [
    ('app.factories', '*'),
]
