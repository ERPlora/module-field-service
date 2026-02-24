"""Tests for field_service models."""
import pytest
from django.utils import timezone

from field_service.models import WorkOrder


@pytest.mark.django_db
class TestWorkOrder:
    """WorkOrder model tests."""

    def test_create(self, work_order):
        """Test WorkOrder creation."""
        assert work_order.pk is not None
        assert work_order.is_deleted is False

    def test_str(self, work_order):
        """Test string representation."""
        assert str(work_order) is not None
        assert len(str(work_order)) > 0

    def test_soft_delete(self, work_order):
        """Test soft delete."""
        pk = work_order.pk
        work_order.is_deleted = True
        work_order.deleted_at = timezone.now()
        work_order.save()
        assert not WorkOrder.objects.filter(pk=pk).exists()
        assert WorkOrder.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, work_order):
        """Test default queryset excludes deleted."""
        work_order.is_deleted = True
        work_order.deleted_at = timezone.now()
        work_order.save()
        assert WorkOrder.objects.filter(hub_id=hub_id).count() == 0


