import inspect

from django.apps import apps

from .settings import app_settings

if app_settings.USE_ASGIREF:
    # asgiref must be installed, its included with Django >= 3.0
    from asgiref.local import Local as local
else:
    from threading import local


_thread_locals = _context = local()


def get_model_by_db_table(db_table):
    for model in apps.get_models():
        if model._meta.db_table == db_table:
            return model

    raise ValueError(f"No model found with db_table {db_table}")


def get_current_tenant():
    return getattr(_context, "tenant", None)


def get_tenant_column(model_class_or_instance: object):
    if inspect.isclass(model_class_or_instance):
        model_class_or_instance = model_class_or_instance()

    try:
        return model_class_or_instance.tenant_field
    except Exception as not_a_tenant_model:
        raise ValueError(
            f"{model_class_or_instance.__class__.__name__} is not an instance or a subclass of TenantModel or does not inherit from TenantMixin"
        ) from not_a_tenant_model


def get_tenant_field(model_class_or_instance: object):
    tenant_column = get_tenant_column(model_class_or_instance)
    all_fields = model_class_or_instance._meta.fields
    try:
        return next(field for field in all_fields if field.column == tenant_column)
    except StopIteration as no_field_found:
        raise ValueError(
            f'No field found in {model_class_or_instance.__class__.__name__} with column name "{tenant_column}"'
        ) from no_field_found


def get_object_tenant(instance):
    field = get_tenant_field(instance)

    if field.primary_key:
        return instance

    return getattr(instance, field.name, None)


def set_object_tenant(instance, value):
    if instance.tenant_value is None and value and not isinstance(value, list):
        setattr(instance, instance.tenant_field, value)


def get_current_tenant_value():
    current_tenant = get_current_tenant()
    if not current_tenant:
        return None

    try:
        current_tenant = list(current_tenant)
    except TypeError:
        return current_tenant.tenant_value

    values = []
    for t in current_tenant:
        values.append(t.tenant_value)
    return values


def get_tenant_filters(table, filters=None):
    filters = filters or {}

    current_tenant_value = get_current_tenant_value()

    if not current_tenant_value:
        return filters

    if isinstance(current_tenant_value, list):
        filters[f"{get_tenant_column(table)}__in"] = current_tenant_value
    else:
        filters[get_tenant_column(table)] = current_tenant_value

    return filters


def set_current_tenant(tenant):
    setattr(_context, "tenant", tenant)


def unset_current_tenant():
    setattr(_context, "tenant", None)
