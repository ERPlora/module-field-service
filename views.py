"""
Field Service Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import WorkOrder

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('field_service', 'dashboard')
@htmx_view('field_service/pages/index.html', 'field_service/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_work_orders': WorkOrder.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# WorkOrder
# ======================================================================

WORK_ORDER_SORT_FIELDS = {
    'title': 'title',
    'reference': 'reference',
    'status': 'status',
    'priority': 'priority',
    'description': 'description',
    'scheduled_date': 'scheduled_date',
    'created_at': 'created_at',
}

def _build_work_orders_context(hub_id, per_page=10):
    qs = WorkOrder.objects.filter(hub_id=hub_id, is_deleted=False).order_by('title')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'work_orders': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'title',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_work_orders_list(request, hub_id, per_page=10):
    ctx = _build_work_orders_context(hub_id, per_page)
    return django_render(request, 'field_service/partials/work_orders_list.html', ctx)

@login_required
@with_module_nav('field_service', 'work_orders')
@htmx_view('field_service/pages/work_orders.html', 'field_service/partials/work_orders_content.html')
def work_orders_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'title')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = WorkOrder.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(reference__icontains=search_query) | Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(status__icontains=search_query))

    order_by = WORK_ORDER_SORT_FIELDS.get(sort_field, 'title')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['title', 'reference', 'status', 'priority', 'description', 'scheduled_date']
        headers = ['Title', 'Reference', 'Status', 'Priority', 'Description', 'Scheduled Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='work_orders.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='work_orders.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'field_service/partials/work_orders_list.html', {
            'work_orders': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'work_orders': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def work_order_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        priority = request.POST.get('priority', '').strip()
        scheduled_date = request.POST.get('scheduled_date') or None
        completed_date = request.POST.get('completed_date') or None
        address = request.POST.get('address', '').strip()
        assigned_to = request.POST.get('assigned_to', '').strip()
        notes = request.POST.get('notes', '').strip()
        obj = WorkOrder(hub_id=hub_id)
        obj.reference = reference
        obj.title = title
        obj.description = description
        obj.status = status
        obj.priority = priority
        obj.scheduled_date = scheduled_date
        obj.completed_date = completed_date
        obj.address = address
        obj.assigned_to = assigned_to
        obj.notes = notes
        obj.save()
        return _render_work_orders_list(request, hub_id)
    return django_render(request, 'field_service/partials/panel_work_order_add.html', {})

@login_required
def work_order_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(WorkOrder, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.reference = request.POST.get('reference', '').strip()
        obj.title = request.POST.get('title', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.priority = request.POST.get('priority', '').strip()
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.completed_date = request.POST.get('completed_date') or None
        obj.address = request.POST.get('address', '').strip()
        obj.assigned_to = request.POST.get('assigned_to', '').strip()
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_work_orders_list(request, hub_id)
    return django_render(request, 'field_service/partials/panel_work_order_edit.html', {'obj': obj})

@login_required
@require_POST
def work_order_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(WorkOrder, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_work_orders_list(request, hub_id)

@login_required
@require_POST
def work_orders_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = WorkOrder.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_work_orders_list(request, hub_id)


@login_required
@permission_required('field_service.manage_settings')
@with_module_nav('field_service', 'settings')
@htmx_view('field_service/pages/settings.html', 'field_service/partials/settings_content.html')
def settings_view(request):
    return {}

