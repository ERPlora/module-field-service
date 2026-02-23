from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

WO_STATUS = [
    ('pending', _('Pending')),
    ('assigned', _('Assigned')),
    ('in_progress', _('In Progress')),
    ('completed', _('Completed')),
    ('cancelled', _('Cancelled')),
]

class WorkOrder(HubBaseModel):
    reference = models.CharField(max_length=50, verbose_name=_('Reference'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=20, default='pending', choices=WO_STATUS, verbose_name=_('Status'))
    priority = models.CharField(max_length=20, default='medium', verbose_name=_('Priority'))
    scheduled_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Scheduled Date'))
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Completed Date'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    assigned_to = models.UUIDField(null=True, blank=True, verbose_name=_('Assigned To'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'field_service_workorder'

    def __str__(self):
        return self.title

