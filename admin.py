from django.contrib import admin

from .models import WorkOrder

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['reference', 'title', 'status', 'priority', 'created_at']
    search_fields = ['reference', 'title', 'description', 'status']
    readonly_fields = ['created_at', 'updated_at']

