-- ============================
-- INVENTORY MANAGEMENT SYSTEM - FINAL VERSION
-- ============================
-- --uom:unit of measurement.

DROP DATABASE IF EXISTS ims_db;
CREATE DATABASE ims_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ims_db;

-- ROLES
CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name ENUM('ADMIN', 'INVENTORY_MANAGER', 'PURCHASE_MANAGER','REQUESTER') UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='User roles defining permissions';

-- USERS
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    failed_attempts INT NULL DEFAULT 0,
    locked_until DATETIME NULL,
    last_login DATETIME DEFAULT NULL,
    last_logout DATETIME DEFAULT NULL,
    deleted_at DATETIME DEFAULT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='System users linked to roles';

CREATE INDEX idx_users_role_id ON users(role_id);

-- AUDIT LOGS
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Tracks user actions';

CREATE INDEX idx_audit_user_id ON audit_logs(user_id);

-- WAREHOUSES
CREATE TABLE warehouses (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_name VARCHAR(255) NOT NULL,
    warehouse_location VARCHAR(255) NOT NULL,
    manager_id INT,
    capacity INT CHECK (capacity >= 0),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (manager_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Warehouse master data';

CREATE INDEX idx_warehouse_manager_id ON warehouses(manager_id);

-- STORAGE SECTIONS
CREATE TABLE storage_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT NOT NULL,
    section_name VARCHAR(100) NOT NULL,
    capacity INT DEFAULT NULL CHECK (capacity IS NULL OR capacity >= 0),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Subsections of warehouses';

CREATE INDEX idx_section_warehouse_id ON storage_sections(warehouse_id);


CREATE TABLE stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_name VARCHAR(255) NOT NULL,
    section_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    status ENUM('AVAILABLE', 'RESERVED', 'DAMAGED', 'EXPIRED') DEFAULT 'AVAILABLE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (section_id) REFERENCES storage_sections(section_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Tracks stock of products across warehouses and sections';


-- CATEGORIES
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(150) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Product categories';

-- PRODUCTS
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) DEFAULT 0.00 CHECK (price >= 0),
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    uom TEXT NOT NULL,
    status ENUM('AVAILABLE', 'UNAVAILABLE') DEFAULT 'AVAILABLE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Product details';

CREATE INDEX idx_products_category_id ON products(category_id);

-- PROJECTS
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Project records used in requisitions';

-- REQUISITION
CREATE TABLE requisition (
    requisition_id INT AUTO_INCREMENT PRIMARY KEY,
    requester_id INT NOT NULL,
    project_id INT,
    status ENUM('PENDING','APPROVED','REJECTED','ISSUED','CANCELLED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    submitted_at DATETIME DEFAULT NULL,
    approved_at DATETIME DEFAULT NULL,
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (requester_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Material requisitions';

CREATE INDEX idx_requisition_requester_id ON requisition(requester_id);

-- REQUISITION ITEMS
CREATE TABLE requisition_items (
    req_item_id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (requisition_id) REFERENCES requisition(requisition_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Items inside requisitions';

CREATE INDEX idx_req_items_requisition_id ON requisition_items(requisition_id);

-- SUPPLIERS
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(100) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL
) ENGINE=InnoDB COMMENT='Suppliers providing materials';

-- PURCHASE ORDERS
CREATE TABLE purchase_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    created_by_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_delivery_date DATE DEFAULT NULL,
    status ENUM('PENDING', 'APPROVED', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    total_amount DECIMAL(10, 2) DEFAULT 0.00 CHECK (total_amount >= 0),
    deleted_at DATETIME DEFAULT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Purchase orders from suppliers';

CREATE INDEX idx_po_supplier_id ON purchase_orders(supplier_id);

-- PURCHASE ORDER ITEMS
CREATE TABLE purchase_order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    uom TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES purchase_orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Products in each purchase order';

CREATE INDEX idx_poi_order_id ON purchase_order_items(order_id);

-- INVOICES
CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    invoice_number VARCHAR(100) NOT NULL UNIQUE,
    invoice_date DATE NOT NULL,
    due_date DATE DEFAULT NULL,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    status ENUM('UNPAID', 'PAID', 'PARTIALLY_PAID', 'VOID') DEFAULT 'UNPAID',
    file_path VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (order_id) REFERENCES purchase_orders(order_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Supplier invoices for POs';

CREATE INDEX idx_invoice_order_id ON invoices(order_id);

-- PAYMENTS
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    payment_method ENUM('BANK_TRANSFER', 'CHEQUE','CASH') DEFAULT 'BANK_TRANSFER',
    transaction_ref VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Payments made for invoices';

CREATE INDEX idx_payment_invoice_id ON payments(invoice_id);

-- DEFAULT DATA
INSERT INTO roles (role_name, description) VALUES
('ADMIN', 'System administrator with full privileges'),
('INVENTORY_MANAGER', 'Responsible for managing inventory and stock'),
('PURCHASE_MANAGER', 'Handles supplier and purchasing operations'),
('REQUESTER', 'Employee who requests materials or items');

INSERT INTO users (username, password, role_id, status)
VALUES ('root_admin', 'placeholder_hashed_pw', 1, 'ACTIVE');


# CREATE TABLE goods_receipts (--?
#     grn_id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT NOT NULL,
#     received_by INT NOT NULL,
#     received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     status ENUM('OPEN','POSTED','CANCELLED') DEFAULT 'OPEN',
#     notes VARCHAR(255),
#     FOREIGN KEY (order_id) REFERENCES purchase_orders(order_id)
#         ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (received_by) REFERENCES users(user_id)
#         ON DELETE RESTRICT ON UPDATE CASCADE
# ) ENGINE=InnoDB;
#
# CREATE TABLE goods_receipt_items (--?
#     grn_item_id INT AUTO_INCREMENT PRIMARY KEY,
#     grn_id INT NOT NULL,
#     product_id INT NOT NULL,
#     uom_id INT NOT NULL,
#     quantity DECIMAL(18,6) NOT NULL,
#     warehouse_id INT NOT NULL,
#     section_id INT NULL,
#     bin_id INT NULL,
#     lot_id INT NULL,
#     FOREIGN KEY (grn_id) REFERENCES goods_receipts(grn_id)
#         ON DELETE CASCADE ON UPDATE CASCADE,
#     FOREIGN KEY (product_id) REFERENCES products(product_id)
#         ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
#         ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
#         ON DELETE RESTRICT ON UPDATE CASCADE,
#     FOREIGN KEY (section_id) REFERENCES storage_sections(section_id)
#         ON DELETE SET NULL ON UPDATE CASCADE,
#     FOREIGN KEY (bin_id) REFERENCES bins(bin_id)
#         ON DELETE SET NULL ON UPDATE CASCADE,
#     FOREIGN KEY (lot_id) REFERENCES lot(lot_id)
#         ON DELETE SET NULL ON UPDATE CASCADE
# ) ENGINE=InnoDB;







