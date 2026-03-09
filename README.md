# Field Service

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `field_service` |
| **Version** | `1.0.0` |
| **Icon** | `navigate-outline` |
| **Dependencies** | None |

## Models

### `WorkOrder`

WorkOrder(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, reference, title, description, status, priority, scheduled_date, completed_date, address, assigned_to, notes)

| Field | Type | Details |
|-------|------|---------|
| `reference` | CharField | max_length=50 |
| `title` | CharField | max_length=255 |
| `description` | TextField | optional |
| `status` | CharField | max_length=20, choices: pending, assigned, in_progress, completed, cancelled |
| `priority` | CharField | max_length=20 |
| `scheduled_date` | DateTimeField | optional |
| `completed_date` | DateTimeField | optional |
| `address` | TextField | optional |
| `assigned_to` | UUIDField | max_length=32, optional |
| `notes` | TextField | optional |

## URL Endpoints

Base path: `/m/field_service/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `routes/` | `routes` | GET |
| `work_orders/` | `work_orders_list` | GET |
| `work_orders/add/` | `work_order_add` | GET/POST |
| `work_orders/<uuid:pk>/edit/` | `work_order_edit` | GET |
| `work_orders/<uuid:pk>/delete/` | `work_order_delete` | GET/POST |
| `work_orders/bulk/` | `work_orders_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `field_service.view_workorder` | View Workorder |
| `field_service.add_workorder` | Add Workorder |
| `field_service.change_workorder` | Change Workorder |
| `field_service.delete_workorder` | Delete Workorder |
| `field_service.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_workorder`, `change_workorder`, `view_workorder`
- **employee**: `add_workorder`, `view_workorder`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Work Orders | `construct-outline` | `work_orders` | No |
| Routes | `navigate-outline` | `routes` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_work_orders`

List field service work orders.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | pending, assigned, in_progress, completed, cancelled |
| `priority` | string | No |  |
| `limit` | integer | No |  |

### `create_work_order`

Create a field service work order.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes |  |
| `description` | string | No |  |
| `priority` | string | No |  |
| `address` | string | No |  |
| `scheduled_date` | string | No |  |
| `assigned_to` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  field_service/
    css/
    js/
  icons/
    icon.svg
templates/
  field_service/
    pages/
      dashboard.html
      index.html
      routes.html
      settings.html
      work_order_add.html
      work_order_edit.html
      work_orders.html
    partials/
      dashboard_content.html
      panel_work_order_add.html
      panel_work_order_edit.html
      routes_content.html
      settings_content.html
      work_order_add_content.html
      work_order_edit_content.html
      work_orders_content.html
      work_orders_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
