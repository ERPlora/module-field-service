"""AI tools for the Field Service module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListWorkOrders(AssistantTool):
    name = "list_work_orders"
    description = "List field service work orders."
    module_id = "field_service"
    required_permission = "field_service.view_workorder"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "pending, assigned, in_progress, completed, cancelled"},
            "priority": {"type": "string"}, "limit": {"type": "integer"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from field_service.models import WorkOrder
        qs = WorkOrder.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('priority'):
            qs = qs.filter(priority=args['priority'])
        limit = args.get('limit', 20)
        return {"work_orders": [{"id": str(w.id), "reference": w.reference, "title": w.title, "status": w.status, "priority": w.priority, "scheduled_date": str(w.scheduled_date) if w.scheduled_date else None, "address": w.address} for w in qs.order_by('-created_at')[:limit]]}


@register_tool
class CreateWorkOrder(AssistantTool):
    name = "create_work_order"
    description = "Create a field service work order."
    module_id = "field_service"
    required_permission = "field_service.add_workorder"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "title": {"type": "string"}, "description": {"type": "string"},
            "priority": {"type": "string"}, "address": {"type": "string"},
            "scheduled_date": {"type": "string"}, "assigned_to": {"type": "string"},
        },
        "required": ["title"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from field_service.models import WorkOrder
        w = WorkOrder.objects.create(title=args['title'], description=args.get('description', ''), priority=args.get('priority', 'normal'), address=args.get('address', ''), scheduled_date=args.get('scheduled_date'), assigned_to=args.get('assigned_to'))
        return {"id": str(w.id), "reference": w.reference, "created": True}


@register_tool
class UpdateFieldJob(AssistantTool):
    name = "update_field_job"
    description = "Update a field service work order (title, description, status, priority, dates, address, notes)."
    module_id = "field_service"
    required_permission = "field_service.change_workorder"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "job_id": {"type": "string", "description": "Work order ID"},
            "title": {"type": "string", "description": "Job title"},
            "description": {"type": "string", "description": "Job description"},
            "status": {"type": "string", "description": "pending, assigned, in_progress, completed, cancelled"},
            "priority": {"type": "string", "description": "Job priority (e.g. low, medium, high, urgent)"},
            "address": {"type": "string", "description": "Service address"},
            "scheduled_date": {"type": "string", "description": "Scheduled date/time (ISO 8601)"},
            "completed_date": {"type": "string", "description": "Completion date/time (ISO 8601)"},
            "assigned_to": {"type": "string", "description": "UUID of the assigned employee"},
            "notes": {"type": "string", "description": "Internal notes"},
        },
        "required": ["job_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from field_service.models import WorkOrder
        try:
            w = WorkOrder.objects.get(id=args['job_id'])
        except WorkOrder.DoesNotExist:
            return {"error": "Work order not found"}
        fields = []
        for field in ('title', 'description', 'status', 'priority', 'address',
                      'scheduled_date', 'completed_date', 'assigned_to', 'notes'):
            if field in args:
                setattr(w, field, args[field])
                fields.append(field)
        if fields:
            fields.append('updated_at')
            w.save(update_fields=fields)
        return {"id": str(w.id), "reference": w.reference, "status": w.status, "updated": True}


@register_tool
class DeleteFieldJob(AssistantTool):
    name = "delete_field_job"
    description = "Delete (soft-delete) a field service work order."
    module_id = "field_service"
    required_permission = "field_service.delete_workorder"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "job_id": {"type": "string", "description": "Work order ID"},
        },
        "required": ["job_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from field_service.models import WorkOrder
        try:
            w = WorkOrder.objects.get(id=args['job_id'])
        except WorkOrder.DoesNotExist:
            return {"error": "Work order not found"}
        reference = w.reference
        w.is_deleted = True
        w.status = 'cancelled'
        w.save(update_fields=['is_deleted', 'status', 'updated_at'])
        return {"deleted": True, "reference": reference}


@register_tool
class BulkCreateFieldJobs(AssistantTool):
    name = "bulk_create_field_jobs"
    description = "Create multiple field service work orders at once (max 50)."
    module_id = "field_service"
    required_permission = "field_service.add_workorder"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "jobs": {
                "type": "array",
                "description": "List of work orders to create (max 50)",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "priority": {"type": "string"},
                        "address": {"type": "string"},
                        "scheduled_date": {"type": "string", "description": "ISO 8601 date/time"},
                        "assigned_to": {"type": "string", "description": "Employee UUID"},
                    },
                    "required": ["title"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["jobs"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from field_service.models import WorkOrder
        items = args['jobs'][:50]
        created = []
        for item in items:
            w = WorkOrder.objects.create(
                title=item['title'],
                description=item.get('description', ''),
                priority=item.get('priority', 'medium'),
                address=item.get('address', ''),
                scheduled_date=item.get('scheduled_date'),
                assigned_to=item.get('assigned_to'),
            )
            created.append({"id": str(w.id), "reference": w.reference, "title": w.title})
        return {"created": len(created), "jobs": created}
