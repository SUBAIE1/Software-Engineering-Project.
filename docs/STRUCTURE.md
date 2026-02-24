"""Project structure documentation."""

# INVENTORY MANAGEMENT SYSTEM - PROJECT STRUCTURE

```
IMS/
├── config/                              # Configuration
│   ├── __init__.py
│   ├── database_connection.py           # Singleton DB connection
│   └── Database.sql                     # Complete schema
│
├── src/                                 # Main source code
│   ├── __init__.py
│   ├── main.py                          # Application entry point
│   │
│   ├── models/                          # Data models (ORM-like)
│   │   ├── __init__.py
│   │   ├── product.py                   # Product model
│   │   ├── warehouse.py                 # Warehouse, StorageSection, Stock
│   │   ├── user.py                      # User, Admin, InventoryManager, Role
│   │   └── requisition.py               # Requisition, RequisitionItem
│   │
│   ├── repositories/                    # Data access layer
│   │   ├── __init__.py
│   │   ├── product_repository.py        # ProductRepository
│   │   ├── user_repository.py           # UserRepository
│   │   ├── warehouse_repository.py      # WarehouseRepository, StorageSectionRepository
│   │   └── requisition_repository.py    # RequisitionRepository, RequisitionItemRepository
│   │
│   ├── services/                        # Business logic layer
│   │   ├── __init__.py
│   │   ├── inventory_service.py         # Warehouse & stock management
│   │   ├── auth_service.py              # Authentication & validation
│   │   ├── reporting_service.py         # Reports generation
│   │   └── log_service.py               # Audit logging
│   │
│   ├── utils/                           # Utilities & helpers
│   │   ├── __init__.py
│   │   ├── validators.py                # Input validation
│   │   ├── hashing.py                   # Password hashing
│   │   └── migrations.py                # Database migrations
│   │
│   ├── gui/                             # GUI components (Tkinter)
│   │   ├── __init__.py
│   │   ├── admin.py                     # Admin interface
│   │   ├── product.py                   # Product management UI
│   │   ├── warehouse.py                 # Warehouse management UI
│   │   └── stock.py                     # Stock management UI
│   │
│   └── purchase_orders/                 # Purchase order system
│       ├── __init__.py
│       ├── purchase_order.py            # PO model & operations
│       ├── invoice.py                   # Invoice creation & tracking
│       ├── payment.py                   # Payment processing
│       └── supplier.py                  # Supplier management
│
├── services/                            # Backward compatibility proxy
│   ├── __init__.py
│   ├── auth_service.py                  # Points to src/services/
│   └── log_service.py                   # Points to src/services/
│
├── docs/                                # Documentation
│   ├── ER-DIAGRAM                       # Database ER diagram
│   └── API.md                           # API documentation
│
├── logs/                                # Application logs (created at runtime)
│   └── ims.log
│
├── data/                                # Data files (created at runtime)
│
├── connection.py                        # Central connection proxy
├── export_reports.py                    # Report export utility
├── settings.py                          # Application settings
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
└── README.md                            # Project documentation

```

## Architecture Layers

### 1. Models (src/models/)
- Pure data models representing business entities
- No database operations
- Include validation logic

### 2. Repositories (src/repositories/)
- Data access layer
- Handles all database queries
- Implements CRUD operations
- Returns dictionaries or model instances

### 3. Services (src/services/)
- Business logic layer
- Coordinates between repositories
- Handles complex operations
- No direct database access

### 4. Utils (src/utils/)
- Shared utilities
- Validators, hashers, helpers
- No business logic

### 5. GUI (src/gui/)
- User interface components
- Uses services for operations
- Tkinter based

### 6. Purchase Orders (src/purchase_orders/)
- Specialized domain for PO management
- Includes invoicing and payments
- Separate module for modularity

## Import Conventions

### For Models
```python
from src.models.product import Product
from src.models.warehouse import Warehouse, StorageSection, Stock
from src.models.user import User, Admin, Role
```

### For Repositories
```python
from src.repositories.product_repository import ProductRepository
from src.repositories.warehouse_repository import WarehouseRepository
```

### For Services
```python
from src.services.inventory_service import InventoryService
from src.services.auth_service import AuthService
```

### For Utilities
```python
from src.utils.validators import validate_email
from src.utils.hashing import hash_password
```

## Backward Compatibility

- `connection.py` - Proxy to config.database_connection
- `services/` directory - Points to src/services/
- `export_reports.py` - Maintains original location

## Configuration

- `config/database_connection.py` - Singleton pattern
- `settings.py` - Environment-based configuration
- `.env` - Local environment variables
