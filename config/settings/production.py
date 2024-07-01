# flake8: noqa
from .common import *

DEBUG = False
INSTALLED_APPS.insert(4, "whitenoise.runserver_nostatic")
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
