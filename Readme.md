# Car Rental API

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-blueviolet)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

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

See the architecture diagram in `https://github.com/Mason-MSE/Car-rental/blob/main/architecture.pdf` for visual representation.

## Database Design

The database uses PostgreSQL (or compatible) with SQLAlchemy ORM. Key tables include:

- **user**: id, full_name, password (hashed), email, phone, status.
- **user_profile**: Linked to user, includes address, DOB, nationality, emergency contacts.
- **driver_license**: Linked to user, license_pic, expire_date, is_verified.
- **role**: id, role_name.
- **resource**: id, resource_name, resource_link, resource_method.
- **user_role** and **role_resource**: Many-to-many for RBAC.
- **car**: id, make, model, year, mileage, is_available, min/max_rent_days, location_id, category_id.
- **location**: id, location_name, street, zipcode, city, state.
- **car_category**: id, category_name.
- **booking**: id, user_id, car_id, insurance_id, start/end_date, pickup/drop_location, status (enum: pending, approved, etc.).
- **rent_fee**: Linked to booking, base_amount, insurance_amount, late_fee, discount, taxes, total.
- **payment**: Linked to booking/rent_fee, amount, date, method (enum), status.
- **insurance**: Linked to booking/user, type, policy_number, provider, coverage, premium.
- **insurance_catalogue** and **insurance_price**: Catalogs for insurance options.
- **insurance_company**: Company details.

All tables include create_time, modify_time, is_deleted for auditing/soft deletes.

See ERD in [Database Design PDF](https://github.com/Mason-MSE/Car-rental/blob/main/database_desgin.pdf).

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for development)
- Virtualenv or Poetry for dependency management

### Steps
1. Clone the repository:
    git clone https://github.com/Mason-MSE/Car-rental.git
    cd Car-rental