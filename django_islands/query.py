from django.db.models import Q
from django.db.models.sql.constants import GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.where import WhereNode

from .utils import get_current_tenant, get_tenant_filters


def add_tenant_filters_on_query(obj):
    current_tenant = get_current_tenant()

    if current_tenant:
        try:
            filters = get_tenant_filters(obj.model)
            obj.add_q(Q(**filters))
        except ValueError:
            pass


def wrap_get_compiler(base_get_compiler):
    # Adds tenant filters to the query object
    def get_compiler(obj, *args, **kwargs):
        add_tenant_filters_on_query(obj)
        return base_get_compiler(obj, *args, **kwargs)

    get_compiler._sign = "get_compiler django-multitenant"
    return get_compiler


def wrap_update_batch(base_update_batch):
    # Written to decorate the update_batch method of the UpdateQuery class to add tenant_id filters.
    # Since add tenant_filters method must be executed before the execute_sql method, we have to
    # copy and rewrite the update_batch method.
    # CAUTION: Since source is copied, UpdateQuery.update_batch method should be tracked
    def update_batch(obj, pk_list, values, using):
        obj.add_update_values(values)
        for offset in range(0, len(pk_list), GET_ITERATOR_CHUNK_SIZE):
            obj.where = WhereNode()
            obj.add_q(Q(pk__in=pk_list[offset : offset + GET_ITERATOR_CHUNK_SIZE]))
            add_tenant_filters_on_query(obj)
            obj.get_compiler(using).execute_sql(NO_RESULTS)

    update_batch._sign = "update_batch django-multitenant"
    return update_batch
