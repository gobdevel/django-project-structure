# flake8: noqa
from .common import *

DEBUG = True

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
#     "rest_framework.authentication.SessionAuthentication",
# )

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
    "rest_framework.renderers.BrowsableAPIRenderer",
)

CORS_ORIGIN_WHITELIST = ["http://localhost:4200", "http://127.0.0.1:4200"]

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
