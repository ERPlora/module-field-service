# Field Service Module

Field work orders, routes, and mobile technician management.

## Features

- Create and manage field work orders with priority levels
- Track work order status through lifecycle: pending, assigned, in progress, completed, cancelled
- Assign work orders to technicians
- Record scheduling and completion dates
- Capture service address and detailed descriptions
- Plan and manage service routes
- Dashboard with overview of field service activity

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Field Service > Settings**

## Usage

Access via: **Menu > Field Service**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/field_service/dashboard/` | Overview of field service activity and work order status |
| Work Orders | `/m/field_service/work_orders/` | List, create, and manage work orders |
| Routes | `/m/field_service/routes/` | Plan and manage service routes |
| Settings | `/m/field_service/settings/` | Configure field service module settings |

## Models

| Model | Description |
|-------|-------------|
| `WorkOrder` | Field service work order with reference, title, status, priority, scheduling, address, and assignment |

## Permissions

| Permission | Description |
|------------|-------------|
| `field_service.view_workorder` | View work orders |
| `field_service.add_workorder` | Create new work orders |
| `field_service.change_workorder` | Edit existing work orders |
| `field_service.delete_workorder` | Delete work orders |
| `field_service.manage_settings` | Manage field service module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
