# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.db import models

# from audit_log.models import AuthStampedModel
# from audit_log.models.managers import AuditLog

from django_extensions.db.models import TimeStampedModel

from model_utils import Choices
from model_utils.models import TimeFramedModel
from model_utils.fields import StatusField
from model_utils.managers import QueryManager

from safedelete.models import SafeDeleteModel


class CategoryModel(models.Model):
    """Category abstract base model class

    An abstract base class model with a ``category`` field that
    automatically uses a ``CATEGORY`` class attribute of choices.
    """
    category = StatusField(choices_name='CATEGORY')

    class Meta:
        abstract = True


class StatusModel(model.Model):
    """Status abstract base model class

    An abstract base class model with a ``status`` field that
    automatically uses a ``STATUS`` class attribute of choices.
    """
    status = StatusField(choices_name='STATUS')

    class Meta:
        abstract = True


def add_category_query_managers(sender, **kwargs):
    """
    Add a QueryManager for each status item dynamically.
    """
    if not issubclass(sender, StatusModel):
        return

    # First, get current manager name...
    default_manager = sender._meta.default_manager

    for value, display in getattr(sender, 'CATEGORY', ()):
        if _field_exists(sender, value):
            raise ImproperlyConfigured(
                "StatusModel: Model '%s' has a field named '%s' which "
                "conflicts with a status of the same name."
                % (sender.__name__, value)
            )
        sender.add_to_class(value, QueryManager(status=value))

    # ...then, put it back, as add_to_class is modifying the default manager!
    sender._meta.default_manager_name = default_manager.name


def add_status_query_managers(sender, **kwargs):
    """
    Add a QueryManager for each status item dynamically.
    """
    if not issubclass(sender, StatusModel):
        return

    # First, get current manager name...
    default_manager = sender._meta.default_manager

    for value, display in getattr(sender, 'STATUSES', ()):
        if _field_exists(sender, value):
            raise ImproperlyConfigured(
                "StatusModel: Model '%s' has a field named '%s' which "
                "conflicts with a status of the same name."
                % (sender.__name__, value)
            )
        sender.add_to_class(value, QueryManager(status=value))

    # ...then, put it back, as add_to_class is modifying the default manager!
    sender._meta.default_manager_name = default_manager.name


models.signals.class_prepared.connect(add_category_query_managers)
models.signals.class_prepared.connect(add_status_query_managers)


class BaseModel(
    TimeStampedModel,
    # AuthStampedModel,
    SafeDeleteModel
):
    # audit_log = AuditLog()

    class Meta:
        abstract = True


class NoteModel(BaseModel):
    text = models.CharField(
        'Text',
        max_length=512,
        blank=True,
        null=True,
        default='',
    )

    class Meta:
        abstract = True


class AttachmentModel(BaseModel):
    UPLOAD_TO = None

    file = models.FileField(
        upload_to=UPLOAD_TO,
        blank=True,
        null=True,
        default='',
    )

    class Meta:
        abstract = True
