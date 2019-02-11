from .base import INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK

# Maps can be requested using <map_slug>.localhost.
ALLOWED_HOSTS = [".localhost"]

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", "django_extensions")

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
    "rest_framework.renderers.BrowsableAPIRenderer"
)

SECRET_KEY = "d)1)w5(&@^a=avczu_j$y0a)!-zq%v_vfywfuzv8rq_51t)-^+"

SHELL_PLUS_POST_IMPORTS = [("app.factories", "*")]
