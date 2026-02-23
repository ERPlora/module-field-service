"""
Field Service Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('field_service', 'dashboard')
@htmx_view('field_service/pages/dashboard.html', 'field_service/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('field_service', 'work_orders')
@htmx_view('field_service/pages/work_orders.html', 'field_service/partials/work_orders_content.html')
def work_orders(request):
    """Work Orders view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('field_service', 'routes')
@htmx_view('field_service/pages/routes.html', 'field_service/partials/routes_content.html')
def routes(request):
    """Routes view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('field_service', 'settings')
@htmx_view('field_service/pages/settings.html', 'field_service/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

