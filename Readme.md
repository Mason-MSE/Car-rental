# Car Rental System

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-blueviolet)](https://www.sqlalchemy.org/)

## Project Description

This is a backend API for a car rental system built with FastAPI, SQLAlchemy, and Pydantic. It supports user registration, authentication, role-based access control (RBAC), car management, booking rentals, payment processing, and insurance handling. The system differentiates between customer and admin roles, with admins managing cars, bookings, and roles/resources.

Key features include:
- User registration with driver license upload and face identification (simulated).
- Viewing and booking available cars with fee calculation.
- Admin approval/rejection of bookings with notifications.
- Real-time location services (e.g., Bluetooth support for car tracking).
- Soft deletes and audit timestamps on all entities.

The architecture follows a layered design inspired by Clean Architecture, with dependency injection via FastAPI's Depends. It incorporates design patterns like Observer for notifications and Factory for database connections.

## Features

### User Management
- Registration and login with JWT authentication.
- Role assignment (Customer, Admin).
- Profile management including address, emergency contacts, and preferences.

### Car Management
- Admins can add, edit, delete, or mark cars as unavailable.
- Car details: make, model, year, mileage, availability, min/max rent days, category, location.

### Rental Booking
- Customers view available cars and select rental periods.
- Automatic fee calculation (base, insurance, taxes, discounts, late fees).
- Booking status: pending, approved, rejected, completed.

### Payment and Insurance
- Integrated payment records with methods (enum) and status.
- Insurance catalogs with types, providers, coverage, and premiums.

### RBAC
- Roles linked to resources and permissions (e.g., car:read, booking:approve).
- Checks enforced via dependencies in routes.

### Notifications
- Uses Observer pattern to notify users on booking approval/rejection (e.g., via email or in-app push).

### Additional
- Factory pattern for database connections (e.g., handling different envs like dev/prod).
- Support for migrations with Alembic.
- API documentation via Swagger UI.

## Architecture

The system uses a layered architecture:

- **Presentation Layer**: FastAPI routers and endpoints.
- **Application Layer**: Services handling business logic (e.g., booking_service.py).
- **Domain Layer**: Interfaces, entities (Pydantic schemas), repositories (abstract).
- **Infrastructure Layer**: SQLAlchemy models, database connections, security (JWT, RBAC).

### Design Patterns

- **Observer Pattern**: Implemented for notification of approval situations. For example, when a booking status changes (e.g., approved or rejected), observers (like email notifier or user dashboard updater) are triggered to inform the customer.
- **Factory Pattern**: Used in database.py to handle database connections. A DatabaseFactory class creates engine and session instances based on environment (e.g., SQLite for testing, PostgreSQL for production).

See the architecture diagram in the picture for visual representation.  

View UML diagrams here:  
![Clinic Architecture](https://github.com/Mason-MSE/Car-rental/blob/main/images/architecture.png)

### Architecture Design Rationale

#### 1. Overview

This architecture follows a **clean, layered design** for a web application backend (likely using Python/FastAPI). It separates concerns into distinct layers, promoting maintainability, testability, and scalability.

#### 2. Architectural Layers & Responsibilities

##### A. Presentation Layer
- **Purpose**: Handles HTTP requests/responses, routing, and input validation.
- **Design Reason**:
  - Thin layer focusing only on API contract and protocol handling.
  - Delegates business logic to services, keeping controllers lean.
  - Enables easy swapping of protocols (REST, GraphQL) without affecting core logic.

##### B. Application Layer
- **Purpose**: Orchestrates use cases, coordinates domain objects, and handles transactions.
- **Design Reason**:
  - Contains **application-specific business logic** (workflows, validations).
  - Acts as mediator between presentation and domain layers.
  - Ensures single responsibility per service (e.g., `BookingService`, `UserService`).

##### C. Domain Layer
- **Purpose**: Contains **core business logic**, entities, rules, and authorization.
- **Design Reason**:
  - **Domain-driven design**: Models real-world business concepts and rules.
  - **Authorization centralization**: RBAC logic is encapsulated here, ensuring consistent policy enforcement.
  - **Framework-agnostic**: Pure business logic without infrastructure dependencies.

##### D. Data Access Layer
- **Purpose**: Maps database tables to Python objects using ORM.
- **Design Reason**:
  - **ORM abstraction**: SQLAlchemy provides database-agnostic operations.
  - **Schema definition**: Centralizes table structures and relationships.
  - **Data integrity**: Enforces constraints at application level.

##### E. Infrastructure Layer
- **Purpose**: Provides technical capabilities (database connections, encryption, logging).
- **Design Reason**:
  - **Dependency inversion**: Concrete implementations of interfaces defined in domain layer.
  - **External service integration**: Handles third-party APIs, email, file storage.
  - **Configuration management**: Centralizes environment-specific settings.

##### F. Data Transfer & Validation Layer
- **Purpose**: Defines data structures for input/output validation and serialization.
- **Design Reason**:
  - **Type safety**: Pydantic schemas ensure data integrity across layer boundaries.
  - **Documentation**: Schemas serve as implicit API documentation.
  - **Separation of concerns**: Different schemas for request, response, and internal use.

##### G. Authorization Foundation
- **Purpose**: Defines the data model for Role-Based Access Control.
- **Design Reason**:
  - **Reusable policy framework**: Centralized permission management.
  - **Flexible authorization**: Supports complex permission hierarchies.
  - **Auditability**: Clear mapping of roles to resources and permissions.

#### 3. Key Architectural Patterns

##### Dependency Direction
- **Dependency rule**: Inner layers (Domain) have no knowledge of outer layers.
- **Benefit**: Domain logic remains pure and testable without framework dependencies.

##### Interface Segregation
- Domain defines **interfaces** (abstract classes).
- Infrastructure provides **concrete implementations**.
- Enables easy mocking for testing and swapping implementations.

##### Separation of Concerns
- **Business logic** → Domain layer
- **Use case orchestration** → Application services
- **Data persistence** → SQLAlchemy models
- **Protocol handling** → Routers/Endpoints

#### 4. Data Flow Example

1. HTTP Request → Router (validates input via Pydantic)  
2. Router → Application Service (orchestrates use case)  
3. Application Service → Domain (business logic + RBAC check)  
4. Domain → Infrastructure (via interfaces) for DB operations  
5. SQLAlchemy Models ←→ Database  
6. Response flows back through layers with proper serialization  

#### 5. Benefits of This Design

##### Testability
- Domain logic can be tested without web framework or database.
- Mock implementations can be injected via interfaces.

##### Maintainability
- Clear boundaries make code easier to understand and modify.
- Changes in one layer (e.g., database) don't cascade through system.

##### Scalability
- Layers can be deployed independently (microservices-ready).
- Horizontal scaling possible at presentation or application layers.

##### Security
- RBAC centralized in domain layer ensures consistent enforcement.
- Input validation at multiple layers (Pydantic + domain validation).

#### 6. Technology Stack Inference
- **Web Framework**: FastAPI or Flask (Pydantic integration)  
- **ORM**: SQLAlchemy  
- **Authentication**: Likely JWT/OAuth2 integrated in security.py  
- **Structure**: Modular Python application with clear separation  

#### 7. Potential Improvements
1. **CQRS Pattern**: Separate commands and queries for complex systems.  
2. **Event-driven architecture**: Add domain events for better decoupling.  
3. **Caching layer**: Between application and infrastructure for performance.  
4. **API versioning**: At router level for backward compatibility.  

#### 8. Summary
This architecture successfully implements **clean architecture principles** with **domain-driven design**. It balances separation of concerns with practical development needs, creating a system that is:  
- **Business-focused** (domain layer centrality)  
- **Technically robust** (layered abstraction)  
- **Flexible** (interface-based dependencies)  
- **Secure** (centralized RBAC)  
- **Maintainable** (clear boundaries and responsibilities)  

### UML Analysis & Design Rationale

#### 1. Overview
This UML diagram represents a **comprehensive car rental business workflow** with **multi-role interaction** (Customer, Registered User, Admin). It captures the end-to-end process from user registration to car return, incorporating both customer-facing and administrative operations.

#### 2. Key System Components & Design Principles

##### A. Multi-Role User Management
Visitor → Registered User → Admin (hierarchical escalation)  

- **Design Reason**: Progressive engagement model
  - **Visitors**: Casual browsers with limited access
  - **Registered Users**: Verified customers with booking capabilities
  - **Admins**: Full system control with RBAC protection
- **Registration Gateway**: Driver license upload ensures compliance and trust  

User Role → Admin Dashboard → Role-Base Access Control  

- **Design Reason**: Security and operational separation
  - **Least privilege principle**: Users only see relevant functions
  - **Admin capabilities**: Car management, booking approval, system configuration
  - **Scalable permissions**: RBAC supports future role additions (e.g., Fleet Manager)

##### C. Car Management Lifecycle
Add car → Edit/Delete → Mark Unavailable → View Available  

- **Design Reason**: Complete asset management
  - **Centralized catalog**: Single source of truth for car inventory
  - **Availability tracking**: Real-time status prevents double-booking
  - **Business rules enforcement**: Minimum/maximum rental days controlled

##### D. Booking Workflow Engine
Create booking → Pending approval → Admin action → Customer notification  

- **Design Reason**: Controlled transaction flow
  - **Approval gateway**: Prevents fraud and ensures resource availability
  - **Status transparency**: Customers receive clear notifications
  - **Exception handling**: Rejection with explanation maintains customer trust

##### E. Smart Rental Execution
Pick up → Real-time tracking → Return → Condition check  

- **Design Reason**: Modern rental experience
  - **Bluetooth integration**: Keyless entry and authentication
  - **Location services**: Theft prevention and fleet optimization
  - **Condition monitoring**: Damage assessment automation

##### F. Financial & Compliance Logic
Calculate fees → Late detection → Extra charges → Payment processing  

- **Design Reason**: Automated revenue protection
  - **Dynamic pricing**: Base rate + insurance + taxes + penalties
  - **Late fee automation**: Eliminates manual tracking
  - **Audit trail**: Clear fee calculation and application

#### 3. Workflow Analysis

##### Customer Journey
1. Registration/Login → 2. Car Search → 3. Booking Request →  
2. Approval Wait → 5. Pickup → 6. Usage → 7. Return → 8. Payment  

- **Seamless experience**: Linear progression with clear milestones
- **Reduced friction**: Minimal steps for returning customers

##### Admin Operations
1. Dashboard → 2. Car Management → 3. Booking Oversight →  
2. Financial Monitoring → 5. System Configuration  

- **Centralized control**: All critical functions in one interface
- **Proactive management**: Real-time visibility into operations

#### 4. Business Logic Integration

##### Insurance Integration
Select car → View insurance options → Include in booking → Calculate premium  

- **Design Reason**: Regulatory compliance and risk management
  - **Mandatory coverage**: Ensures legal requirements met
  - **Optional upgrades**: Revenue opportunity via premium insurance

##### Real-time Services
Bluetooth unlock + GPS tracking + Condition monitoring  

- **Design Reason**: Competitive differentiation
  - **Contactless experience**: Post-pandemic preference
  - **Asset protection**: Proactive theft and damage prevention
  - **Data collection**: Usage patterns for business optimization

##### Notification System
Approval/Rejection notices → Reminders → Return confirmations  

- **Design Reason**: Customer communication automation
  - **Reduced staff workload**: Automated messaging
  - **Improved experience**: Timely, relevant communication

#### 5. Exception Handling Design

##### Late Returns
Return check → Delay detection → Fee calculation → Payment requirement  

- **Automated enforcement**: Eliminates manual follow-up
- **Transparent policies**: Clear fee structure communicated upfront

##### Booking Rejections
Admin review → Reject reason → Customer notification → Alternative suggestions  

- **Graceful denial**: Maintains customer relationship despite rejection
- **Learning opportunity**: Feedback for future approval improvement

#### 6. Technology Implications

##### Required Systems
1. **Mobile App/Web Portal**: Customer interface
2. **Admin Dashboard**: Management interface
3. **Bluetooth Integration**: Vehicle access system
4. **GPS Tracking**: Real-time location services
5. **Payment Gateway**: Transaction processing
6. **Notification Engine**: Email/SMS/push system
7. **Document Verification**: Driver license validation

##### Integration Points
- **Mapping APIs**: Location services for car discovery
- **Payment Processors**: Secure transaction handling
- **Identity Verification**: Third-party license validation
- **Communication APIs**: SMS/email notification delivery

#### 7. Business Benefits

##### Operational Efficiency
- **Automated workflows**: Reduces manual intervention
- **Real-time visibility**: Improves decision making
- **Scalable processes**: Handles volume increases without additional staff

##### Customer Experience
- **Streamlined booking**: Minimal steps for repeat customers
- **Modern features**: Bluetooth, real-time tracking
- **Transparent communication**: Clear status updates and fee explanations

##### Risk Management
- **Verification gateways**: Driver license validation
- **Approval controls**: Prevents fraudulent bookings
- **Asset protection**: GPS and condition monitoring

#### 8. Potential Enhancements

##### Short-term Improvements
1. **Loyalty Program Integration**: Points system for frequent renters
2. **AI Recommendation Engine**: Suggest cars based on user history
3. **Dynamic Pricing**: Demand-based rate adjustments

##### Long-term Evolution
1. **IoT Integration**: Real-time vehicle diagnostics
2. **Blockchain Contracts**: Smart contracts for rental agreements
3. **Predictive Maintenance**: AI-driven service scheduling
4. **Autonomous Vehicle Integration**: Future-proof for driverless cars

#### 9. Summary
This UML design successfully models a **modern, scalable car rental system** that:

1. **Balances automation with control**: Automated workflows with human oversight points
2. **Serves multiple stakeholders**: Customers, admins, and business owners
3. **Integrates modern technologies**: Bluetooth, GPS, real-time services
4. **Ensures compliance and security**: License verification, RBAC, approval workflows
5. **Optimizes business operations**: Efficient resource utilization and revenue protection

### Database Design

#### Database Design Rationale

##### 1. Overview
This database is designed for a **car rental management system**. It follows a **modular, relational structure** with clear separation of concerns, supporting core business processes such as user management, vehicle inventory, booking, payment, and insurance handling.

##### 2. Core Design Principles

###### A. Normalization
The design adheres to **3NF (Third Normal Form)** to minimize redundancy and ensure data integrity:
- Each entity (user, car, booking, payment, etc.) is stored in its own table.
- Foreign keys are used to establish relationships instead of duplicating data.

###### B. Scalability & Maintainability
- **Soft delete pattern**: Each table includes `is_deleted`, `create_time`, and `modify_time` for auditability and non-destructive deletions.
- **Enum/status fields**: Used for `payment_status`, `booking.status`, etc., allowing easy extension of state logic.
- **Decoupled relationships**: Many-to-many relationships are avoided in core tables; instead, linking tables (e.g., `insurance` linking `user` and `booking`) are used.

###### C. Localization & Compliance
- Tables like `user` include `preferred_language`, `nationality`, and address fields (`state_name`, `zipcode`) to support international users.
- `driver_license` stores license images and verification status for regulatory compliance

##### 3. Table Group Analysis

###### User & Authentication Group
- **`user`**: Central table for user profiles, with `driver_license_id` linking to a separate license table for modularity.
- **`driver_license`**: Isolated storage of sensitive license data, supporting verification workflows.
- **`role` & `resource`**: Support RBAC (Role-Based Access Control) for admin/backend systems.

###### Booking & Rental Group
- **`booking`**: Core transaction table linking `user_id`, `car_id`, and `insurance_id`.
- **`car`**: Vehicle details with availability flag, rental rules (`min/max_rent_days`), and `daily_rate`.
- **`location`**: Reusable address model for pickup/drop-off locations and car storage.

###### Financial & Insurance Group
- **`rent_fee`**: Breakdown of rental costs (base, insurance, tax, discounts), linked to `booking_id`.
- **`payment`**: Tracks actual transactions, linked to `rent_fee_id` and `booking_id`.
- **`insurance`**: Stores policy details per booking, with `insurance_price_id` and `insurance_type` for flexibility.
- **`insurance_category`**: Lookup table for insurance types, promoting reuse.

###### Vehicle Classification Group
- **`car_category`**: Categorizes cars (e.g., SUV, Compact) for filtering and pricing.
- **`insurance_category`**: Similar classification for insurance products.

##### 4. Key Relationships & Business Logic
- **User → Driver License**: One-to-one (one user, one license record).
- **User → Booking**: One-to-many (a user can have multiple bookings).
- **Car → Booking**: One-to-many (a car can be booked multiple times).
- **Booking → Rent Fee → Payment**: One-to-one-to-many (a booking has one fee record, which may have multiple payments).
- **Insurance → Booking & User**: Insurance is tied to a specific booking and user.

##### 5. Improvements & Considerations

###### Strengths
- **Audit-ready**: Every table has timestamp and soft delete.
- **Flexible pricing**: `rent_fee` supports discounts, taxes, and late fees.
- **Localization-ready**: Address and language fields support global operations.

##### 6. Summary
This design is **robust, scalable, and business-ready**. It supports multi-tenancy, compliance, financial tracking, and customer management. The modular approach allows independent updates to user, vehicle, or financial modules without system-wide impact.

See ERD in ![Clinic Database Design](https://github.com/Mason-MSE/Car-rental/blob/main/images/database_design.png)

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for development)
- Virtualenv or Poetry for dependency management

### Steps
1. Clone the repository:
   ```bash
   git clone [link]https://github.com/Mason-MSE/Car-rental.git
2. Enter the project directory::
    ```bash
    cd Car-rental
3. Create and activate virtual environment:
    ```bash
   python -m venv venv
   source venv/bin/activate
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    (Includes fastapi, sqlalchemy, pydantic, alembic, pyjwt, passlib[bcrypt], etc.)
5. Set environment variables (in .env file):
   ```bash
    # Replace with your MySQL credentials
    DB_USER = "root"
    DB_PASSWORD = "rootpassword"
    DB_HOST = "127.0.0.1"
    DB_PORT = "3306"
    DB_NAME = "rental"

    # SQLAlchemy database URL for MySQL
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    execute a script for rental_init.db

    administrator: admin@gmail.com/12345
    customer: Jenny@gmail.com/12345
    
## Running the App
    Run the FastAPI server with uvicorn:
    ```bash
    python ./Car-rental/app.py
    The API will be available at `http://127.0.0.1:8000`.
## API Documentation
   - Access Swagger UI for interactive API docs and testing: 
   - URL: `http://127.0.0.1:8000/docs`
   - You can request API interfaces directly from Swagger, including authentication (OAuth2 with JWT).
   - For Redoc: `http://127.0.0.1:8000/redoc`
## Use Examples
### Register a User (POST /users/create_item)
    ```
        {
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "securepassword",
            "phone": "1234567890"
        }
    ``` 
### Login (POST /api/auth/login)
    Returns JWT token.
### Get Available Cars (GET /cars/available) 
    Requires authentication; filtered by location/date.
### Create Booking (POST /bookings)
    ```
        {
        "car_id": 1,
        "start_date": "2026-02-01T00:00:00",
        "end_date": "2026-02-05T00:00:00",
        "pickup_location": "Airport",
        "drop_location": "City Center"
        }
        Fee calculated automatically; 
        status set to pending. Observer notifies admin.
    ```
### Approve Booking (PATCH /bookings/{id}/approve)
    Admin-only; 
    triggers Observer to notify customer.

## Testing
    Run tests with pytest:
    
    ```bash
    pytest