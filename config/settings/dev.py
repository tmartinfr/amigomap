from .base import INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK
from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", "django_extensions")

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
    "rest_framework.renderers.BrowsableAPIRenderer"
)

SHELL_PLUS_POST_IMPORTS = [("app.factories", "*")]
