import django

# default_app_config is auto detected for versions 3.2 and higher:
# https://docs.djangoproject.com/en/3.2/ref/applications/#for-application-authors
if django.VERSION < (3, 2):
    default_app_config = "django_islands.apps.DjangoIslands"

__all__ = ["default_app_config", "version"]

version = (0, 0, 2)

__version__ = ".".join(map(str, version))
__author__ = "Davi Silva Rafacho"
__copyright__ = "Copyright 2025, Yellow Devs"
__license__ = "MIT"
__maintainer__ = "Davi Silva Rafacho"
__email__ = "davi.s.rafacho.developer@gmail.com"
__status__ = "Production"
