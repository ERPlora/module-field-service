"""
AI context for the Field Service module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Field Service

### Models

**WorkOrder**
- `reference` (str, required), `title` (str, required), `description` (text)
- `status` choices: pending | assigned | in_progress | completed | cancelled (default: pending)
- `priority` (str, default 'medium') — common values: low, medium, high, urgent
- `scheduled_date` (datetime, optional), `completed_date` (datetime, optional)
- `address` (text — on-site location), `assigned_to` (UUID, optional — references LocalUser)
- `notes` (text)

### Key Flows

1. **Create work order**: set reference, title, description, and priority. Status starts as 'pending'.
2. **Assign technician**: set assigned_to (UUID of the technician) and update status to 'assigned'.
3. **Schedule**: set scheduled_date for when the field visit should occur.
4. **On-site execution**: update status to 'in_progress' when the technician starts work.
5. **Complete**: set status to 'completed', fill completed_date with the actual finish datetime.
6. **Cancel**: set status to 'cancelled' with a reason in notes if the order cannot be fulfilled.

### Relationships

- `assigned_to` is a raw UUID (no FK) — maps to LocalUser in the accounts module.
- No sub-models (parts, materials, checklist items) in the current model — use notes field for details.
- Use address field to record the customer site or job location.
"""
