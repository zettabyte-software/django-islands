import logging

from django.db import models

from .mixins import TenantManagerMixin, TenantModelMixin, TenantQuerySet

logger = logging.getLogger(__name__)


class TenantManager(TenantManagerMixin, models.Manager.from_queryset(TenantQuerySet)):
    # This parameter is required to add Tenenat Manager in models in the migrations.
    use_in_migrations = True


class TenantModel(TenantModelMixin, models.Model):
    # Abstract model which all the models related to tenant inherit.

    objects = TenantManager()

    class Meta:
        abstract = True
