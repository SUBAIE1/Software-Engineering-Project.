# Inventory Management System (IMS)

A comprehensive Python-based Inventory Management System built with MySQL for managing warehouses, products, requisitions, and purchase orders.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Overview

The Inventory Management System is a full-featured application designed for managing:
- **Products & Categories**: Track inventory items with categories
- **Warehouses & Storage**: Manage warehouse locations and storage sections
- **Stock Management**: Monitor stock levels across locations
- **Purchase Orders**: Create and manage supplier orders
- **Requisitions**: Handle material requests from employees
- **Users & Roles**: Role-based access control (Admin, Inventory Manager, Purchase Manager, Requester)
- **Audit Logs**: Complete tracking of all user actions
- **Reporting**: Generate comprehensive reports on inventory status

## Features

### Core Functionality
- ✅ User Authentication with account lockout protection
- ✅ Role-based access control (4 roles)
- ✅ Complete product lifecycle management
- ✅ Multi-warehouse support with storage sections
- ✅ Stock tracking and inventory monitoring
- ✅ Purchase order workflow
- ✅ Material requisition system
- ✅ Supplier invoice and payment tracking
- ✅ Comprehensive audit logging
- ✅ CSV export for reports

### Security Features
- Password hashing with SHA-256 and salt
- Account lockout after failed login attempts (configurable)
- Audit trail of all database modifications
- User action logging

## Project Structure

```
IMS/
├── config/                          # Configuration files
│   ├── __init__.py
│   ├── database_connection.py       # MySQL connection class (Singleton pattern)
│   └── Database.sql                 # Complete database schema
├── services/                        # Business logic services
│   ├── __init__.py
│   └── auth_service.py              # Authentication service
├── src/                             # Application source code
│   ├── Main.py                      # Application entry point
│   ├── Admin.py                     # Admin user class
│   ├── User.py                      # Abstract user base class
│   ├── Role.py                      # Role management
│   ├── Auth Service.py              # Authentication implementation
│   ├── PurchaseOrder.py             # Purchase order management
│   ├── PurchaseOrderItems.py        # Purchase order items
│   ├── Invoice.py                   # Invoice utilities
│   ├── Payment.py                   # Payment processing
│   ├── Supplier.py                  # Supplier utilities
│   ├── Stock.py                     # Stock management
│   └── StorageSection.py            # Storage section class
├── docs/                            # Documentation
│   └── ER-DIAGRAM                   # Database entity-relationship diagram
├── system/                          # System files
│   └── file.txt                     # Log/system files
├── .env.example                     # Environment variables template
├── connection.py                    # Central connection module
├── export_reports.py                # Report export utility
├── hashing.py                       # Password hashing utilities
├── inventory_service.py             # Inventory management service
├── logging_config.py                # Application logging configuration
├── migrations.py                    # Database migration utilities
├── product.py                       # Product model
├── product_repository.py            # Product data access
├── reporting_service.py             # Reporting service
├── requisition.py                   # Requisition model
├── requisition_repository.py        # Requisition data access
├── settings.py                      # Application settings
├── user_repository.py               # User data access
├── validators.py                    # Input validation utilities
├── warehouse.py                     # Warehouse model
├── warehouse_repository.py          # Warehouse data access
└── README.md                        # This file
```

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd /Users/subaie/projects/my_python_project/Software-Engineering-Project.
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install mysql-connector-python
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ims_db
DEBUG=False
LOG_LEVEL=INFO
```

## Database Setup

### Step 1: Create the Database
```bash
mysql -u root -p < config/Database.sql
```

This will:
- Create the `ims_db` database
- Create all required tables with proper relationships
- Insert default roles
- Insert default users (root1, pur1)

### Step 2: Verify Database Connection
Run the application to verify the connection:
```bash
python src/Main.py
```

## Usage

### Running the Application
```bash
python src/Main.py
```

### Exporting Reports
```bash
python export_reports.py
```

This generates CSV reports for:
- Inventory Summary
- Warehouse Utilization
- Requisitions
- Low Stock Items
- User Activity

### Using the Services

#### Authentication
```python
from services.auth_service import AuthService

auth_service = AuthService()
result = auth_service.validate_credentials("admin_username", "password")
if result.ok:
    print(f"Logged in as: {result.username}, Role: {result.role}")
```

#### Inventory Management
```python
from inventory_service import InventoryService

inv_service = InventoryService()
warehouses = inv_service.get_all_warehouses()
```

#### Product Management
```python
from product_repository import ProductRepository

repo = ProductRepository()
products = repo.find_all(include_unavailable=False)
```

#### Reporting
```python
from reporting_service import ReportingService

reports = ReportingService()
inventory = reports.get_inventory_summary()
low_stock = reports.get_low_stock_items(threshold=20)
```

## API Documentation

### Database Connection
**File**: `config/database_connection.py`

Singleton pattern implementation for MySQL connection management.

```python
from config.database_connection import DatabaseConnection

db = DatabaseConnection()
connection = db.connect()
```

### Authentication Service
**File**: `services/auth_service.py`

```python
from services.auth_service import AuthService

auth = AuthService()
result = auth.validate_credentials(username, password)
```

### Inventory Service
**File**: `inventory_service.py`

```python
from inventory_service import InventoryService

inv = InventoryService()
inv.add_warehouse(name, location, manager, capacity)
inv.add_storage_section(warehouse_id, section_name, capacity)
```

### Repositories
Data access objects for different entities:

- **ProductRepository**: CRUD operations for products
- **UserRepository**: User account management
- **WarehouseRepository**: Warehouse operations
- **RequisitionRepository**: Requisition management

### Validators
**File**: `validators.py`

```python
from validators import (
    validate_email, 
    validate_phone,
    validate_sku,
    validate_password,
    sanitize_input
)
```

### Password Hashing
**File**: `hashing.py`

```python
from hashing import hash_password, verify_password

hashed, salt = hash_password("mypassword")
is_valid = verify_password("mypassword", hashed, salt)
```

## Database Schema Highlights

### Users Table
- Username as primary key
- Password hashing with salt
- Role-based access (ADMIN, INVENTORY_MANAGER, PURCHASE_MANAGER, REQUESTER)
- Account lockout mechanism
- Audit trail (failed_attempts, last_login, last_logout)

### Products Table
- Product tracking with categories
- UOM (Unit of Measurement)
- Price and quantity management
- Soft delete support (deleted_at)

### Warehouses Table
- Multi-warehouse support
- Storage sections within warehouses
- Manager assignment
- Capacity tracking

### Purchase Orders
- Complete PO lifecycle (PENDING→APPROVED→SHIPPED→DELIVERED)
- Line items with unit pricing
- Tax and discount support
- Supplier tracking

### Requisitions
- Material request workflow
- Status tracking (PENDING→APPROVED→ISSUED)
- Project association
- Requester audit trail

## Configuration

### Environment Variables
```
DB_HOST          # MySQL host (default: localhost)
DB_PORT          # MySQL port (default: 3306)
DB_USER          # MySQL username
DB_PASSWORD      # MySQL password
DB_NAME          # Database name (default: ims_db)
LOCK_THRESHOLD   # Failed login attempts before lock (default: 5)
LOCK_MINUTES     # Account lockout duration (default: 15)
PASSWORD_MIN_LENGTH # Minimum password length (default: 6)
APP_NAME         # Application name
DEBUG            # Debug mode (default: False)
LOG_LEVEL        # Logging level (default: INFO)
LOG_FILE         # Log file path (optional)
```

## Troubleshooting

### Database Connection Issues
1. Verify MySQL is running
2. Check `.env` file credentials
3. Ensure database user has appropriate privileges
4. Check that `ims_db` database exists

### Import Errors
- All modules now correctly reference `connection.DatabaseConnection`
- Ensure `connection.py` exists in project root
- Verify all package `__init__.py` files are present

### Authentication Issues
- Check that users are marked as ACTIVE in the database
- Verify password hashing is consistent
- Check account lockout status with database query

## Recent Fixes

### Bugs Fixed (v1.0.0)
- ✅ Fixed missing `connection.py` module (28+ import errors)
- ✅ Fixed hardcoded bad database credentials
- ✅ Fixed SQL syntax errors (DELET→DELETE)
- ✅ Fixed variable name mismatches
- ✅ Fixed missing function call parentheses
- ✅ Fixed indentation errors
- ✅ Removed broken `src/catagories` file
- ✅ Fixed Main.py missing App class
- ✅ Added proper package `__init__.py` files
- ✅ Centralized database configuration

## Contributing

Guidelines for contributing to the project:

1. **Code Style**: Follow PEP 8
2. **Documentation**: Add docstrings to all functions/classes
3. **Testing**: Test all changes locally before committing
4. **Database**: Keep Database.sql updated with schema changes
5. **Error Handling**: Include proper error handling and logging

## File Checklist

- [ ] Create `.env` file with database credentials
- [ ] Run database initialization: `mysql < config/Database.sql`
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Verify connection: `python src/Main.py`
- [ ] Test reports: `python export_reports.py`

## Support & Issues

For issues or questions:
1. Check the troubleshooting section
2. Review database logs
3. Check application logs in `/logs` directory
4. Verify database schema matches `config/Database.sql`

## Version History

### v1.0.0 (Current)
- Initial release with complete IMS functionality
- Fixed all critical bugs
- Added comprehensive documentation
- Implemented role-based access control
- Added reporting and export features

## License

This project is part of a Software Engineering educational initiative.

---

**Last Updated**: February 25, 2026  
**Maintainers**: Engineering Team
