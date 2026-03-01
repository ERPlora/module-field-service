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
