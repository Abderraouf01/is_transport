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
  
## Section 1 -Tables (Sabrina's Contribution )
This section is all about the main tables that make the system work. They store all the essential info for the Information System—customers, drivers, vehicles, destinations, services, and pricing.

Everything is connected to the UI and HTML templates, so agents can manage data easily without touching the database directly, and do the Crud (create , read,update and delete on each table )

## Implemented features 
Each HTML template lets the agent to do the crud on the main tables plus mentioned in section 1 plus some other tabes like incidents and expeditions .


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

## Section 3 – Factures et Paiements (Ines's Contribution)
This section presents the core business rules and functionalities related to invoice and payment management within the system.

### Implemented Features
- Automatic invoice amount calculation based on the expeditions included in the invoice
- Computation of total paid amount for each invoice
- Calculation of remaining amount to be paid
- Automatic update of invoice status
- PDF generation for invoices and payments

### Business Logic
The main business rules are implemented directly at the model level:
- The `Facture` model includes methods to compute the total amount,total payments,remaining balance, and to update its status accordingly.
- The `Paiement`models is linked to both the client and the invoice, ensuring data consistency.
- Any modification in payments automatically impacts the invoice status.
### Views are responisble only for :
- Creating invoices and payments
- Displaying journals and detail views
- Triggering PDF generation

## Section 5 – Reclamation (Ines's Contribution)
This section handles the management of customer complaints (reclamations) and their lifecycle.

### Implemented Features
- Controlled reclamations status management
- Journal view displaying all reclamations
- Detailed view for each reclamation
- Generation of reclamation reports
- Colis can be dynamically added to an existing reclamation through dedicated views.
### Business Logic
The `Reclamation` model contains a method to manage and update the status of a reclamation.
 
### Design Principles
- Business rules are implemented in models
- Views are kept thin (orchestration only)
- UI is never trusted for validation
- Modular and maintainable architecture

## Notes
- UI templates and routing to actions are handled in other sections of the project.
- PDF generation relies on WeasyPrint and HTML templates

