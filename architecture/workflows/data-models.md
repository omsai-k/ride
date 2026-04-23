# Data Models Workflow

## Purpose
Translate RiderComm data requirements into database schema, migrations, and validation models.

## Scope
- User model
- Device model
- Ride session and participant models
- Message and event recording models
- RTC session persistence

## Inputs
- `architecture/data-models.md`
- `architecture/backend.md`
- `architecture/api.md`

## Workflow Steps
1. Review the RiderComm domain and entity relationships.
2. Create normalized database schema and migration scripts.
3. Define ORM models or database access objects.
4. Add validation rules for each data entity.
5. Implement lookup and query patterns for session state.
6. Add indexes and constraints for performance.
7. Document the schema and relationships.

## Deliverables
- Database schema files.
- ORM/entity definitions.
- Migration scripts.
- Data validation logic.

## Validation
- Schema reflects the architecture model accurately.
- Referential integrity is enforced.
- CRUD flows work through the API.

## Handoff
- Provide schema to backend and deployment workflows.
- Share event model structure with monitoring and analytics.
