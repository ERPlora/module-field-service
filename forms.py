from django import forms
from django.utils.translation import gettext_lazy as _

from .models import WorkOrder

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['reference', 'title', 'description', 'status', 'priority', 'scheduled_date', 'completed_date', 'address', 'assigned_to', 'notes']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'title': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'priority': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'scheduled_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'completed_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'assigned_to': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

