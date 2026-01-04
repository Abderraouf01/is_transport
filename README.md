# IS Transport Management System

This project is a Django-based information system for managing transport and delivery operations.

## Project Structure
- core/: main application (business logic)
- is_transport/: project configuration
- db.sqlite3: development database

## Work Distribution
The work was divided internally to ensure good modularity and clean architecture:

- Person A Abderraouf: Section 2 – Expedition business logic
- Person B Yasmine:Section 4 
- Person C Ines: Sections 3 and 5
- Person D Sabrina: UI, templates, CRUD operations

## Section 2 – Expedition (Abderraouf's Contribution)
This section focuses on the core business rules related to expedition management:

### Implemented Features
- Automatic tracking number generation
- Automatic expedition cost calculation
- Controlled expedition status lifecycle
- Business rules enforced at model level
- Thin views (no business logic in views)

### Status Lifecycle

cree → transit → tri → livraison → livree / echec


Invalid transitions are automatically rejected by the model.

### Design Principles
- Business rules are implemented in models
- Views are kept thin (orchestration only)
- UI is never trusted for validation
- Modular and maintainable architecture

## Notes
UI templates and routing to actions are handled in other sections of the project.

