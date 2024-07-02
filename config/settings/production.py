# flake8: noqa
from .common import *

DEBUG = False
INSTALLED_APPS.insert(4, "whitenoise.runserver_nostatic")
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Config based on ENV_NAME environ variable, useful for debugging in docker
ENV_NAME = env.str('ENV_NAME', default='production')
if ENV_NAME == 'DEV':
    DEBUG = True

    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
else:
    DEBUG = False
