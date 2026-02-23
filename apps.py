from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FieldServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'field_service'
    label = 'field_service'
    verbose_name = _('Field Service')

    def ready(self):
        pass
