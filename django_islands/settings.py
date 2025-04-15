from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

SETTINGS_NAMESPACE = "ISLANDS"

USER_SETTINGS = getattr(settings, SETTINGS_NAMESPACE, None)

DEFAULTS = {
    "ALLOW_NULL_TENANT": False,
    "ALLOW_CHANGE_TENANT": False,
    "USE_ASGIREF": False,
}

IMPORT_STRINGS = []

REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    if val is None:
        return None

    if isinstance(val, str):
        return import_from_string(val, setting_name)

    if isinstance(val, list | tuple):
        return [import_from_string(item, setting_name) for item in val]

    return val


def import_from_string(val, setting_name):
    try:
        return import_string(val)
    except ImportError as e:
        msg = f"Could not import '{val}' for API setting '{setting_name}'. {e.__class__.__name__}: {e}."
        raise ImportError(msg) from e


class AppSettings:
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)

        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, SETTINGS_NAMESPACE, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid API setting: '{attr}'")

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        if attr in self.import_strings:
            val = perform_import(val, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                msg = f"The '{setting}' setting has been removed. Please refer to documentation for available settings."
                raise RuntimeError(msg)
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


app_settings = AppSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == SETTINGS_NAMESPACE:
        app_settings.reload()


setting_changed.connect(reload_api_settings)
