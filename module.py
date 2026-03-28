from django.utils.translation import gettext_lazy as _

MODULE_ID = 'field_service'
MODULE_NAME = _('Field Service')
MODULE_VERSION = '1.0.1'
MODULE_ICON = 'material:handyman'
MODULE_DESCRIPTION = _('Field work orders, routes and mobile technicians')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'services'
HAS_MODELS = True

MENU = {
    'label': _('Field Service'),
    'icon': 'navigate-outline',
    'order': 35,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Work Orders'), 'icon': 'construct-outline', 'id': 'work_orders'},
{'label': _('Routes'), 'icon': 'navigate-outline', 'id': 'routes'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'field_service.view_workorder',
'field_service.add_workorder',
'field_service.change_workorder',
'field_service.delete_workorder',
'field_service.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_workorder",
        "change_workorder",
        "view_workorder",
    ],
    "employee": [
        "add_workorder",
        "view_workorder",
    ],
}
