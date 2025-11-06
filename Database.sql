

-- DATABASE INITIALIZATION

DROP DATABASE IF EXISTS ims_db;
CREATE DATABASE ims_db; -- --CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ims_db;

-- ROLES TABLE

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name ENUM('ADMIN', 'INVENTORY_MANAGER', 'PURCHASE_MANAGER','REQUESTER'  ) UNIQUE,
    description VARCHAR(255) DEFAULT NULL
);



-- USERS TABLE
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,             -- hashed password ، in User abstract class
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT NULL,
    last_logout DATETIME DEFAULT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);



-- AUDIT LOGS

CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);



-- REPORTS
-- CREATE TABLE reports (
--     report_id INT AUTO_INCREMENT PRIMARY KEY,
--     report_type ENUM('Inventory', 'Procurement', 'Requisition', 'System', 'Audit') NOT NULL,
--     generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     generated_by INT,
--     file_path VARCHAR(255),
--     FOREIGN KEY (generated_by) REFERENCES users(user_id)
--         ON DELETE SET NULL ON UPDATE CASCADE
-- );


-- WAREHOUSES

CREATE TABLE warehouses (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_name VARCHAR(255) NOT NULL,
    warehouse_location VARCHAR(255) NOT NULL,
    manager_id INT,
    capacity INT DEFAULT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- STORAGE SECTIONS

CREATE TABLE storage_sections (
    --storage manager
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT NOT NULL,
    section_name VARCHAR(100) NOT NULL,
    capacity INT DEFAULT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- CATEGORIES

CREATE TABLE categories (--category for each warehous .....? or just products
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(150) NOT NULL UNIQUE
);



-- PRODUCTS

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) DEFAULT 0.00,
    --quantity INT DEFAULT 0, here ? or in stock
    status ENUM('AVAILABLE', 'UNAVAILABLE') DEFAULT 'AVAILABLE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- STOCK

CREATE TABLE stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_name VARCHAR(255) NOT NULL,
    section_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    product_id INT NOT NULL,
    --quantity INT DEFAULT 0,capasity
    status ENUM('AVAILABLE', 'RESERVED', 'DAMAGED', 'EXPIRED') DEFAULT 'AVAILABLE',
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (section_id) REFERENCES storage_sections(section_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


-- PROJECTS needed for requisitions

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- REQUISITION

CREATE TABLE requisition (
    requisition_id INT AUTO_INCREMENT PRIMARY KEY,
    requester_id INT NOT NULL,
    project_id INT,
    status ENUM('PENDING','APPROVED','REJECTED','ISSUED','CANCELLED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    submitted_at DATETIME DEFAULT NULL,
    approved_at DATETIME DEFAULT NULL,
    --approved_by
    --rejected_reason TEXT DEFAULT NULL,
    FOREIGN KEY (requester_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- REQUISITION ITEMS

CREATE TABLE requisition_items (-- items:products
    req_item_id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    --unit_price DECIMAL(10,2) NOT NULL,
    --remarks TEXT,
    FOREIGN KEY (requisition_id) REFERENCES requisition(requisition_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- SUPPLIERS TABLE
-- Stores information about companies that provide products.
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(100) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- PURCHASE ORDERS TABLE
-- Tracks orders placed with suppliers.
CREATE TABLE purchase_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    created_by_id INT NOT NULL, -- User who created the PO (e.g., Purchase Manager)
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_delivery_date DATE DEFAULT NULL,
    status ENUM('PENDING', 'APPROVED', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    total_amount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- PURCHASE ORDER ITEMS TABLE
-- Junction table for items included in each purchase order.
CREATE TABLE purchase_order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL, -- Price from supplier at time of order
    FOREIGN KEY (order_id) REFERENCES purchase_orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- INVOICES TABLE
-- Tracks invoices received from suppliers for purchase orders.
CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    invoice_number VARCHAR(100) NOT NULL UNIQUE, -- Supplier's invoice #
    invoice_date DATE NOT NULL,
    due_date DATE DEFAULT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('UNPAID', 'PAID', 'PARTIALLY_PAID', 'VOID') DEFAULT 'UNPAID',
    file_path VARCHAR(255) DEFAULT NULL, -- Optional path to a scanned invoice PDF/image
    FOREIGN KEY (order_id) REFERENCES purchase_orders(order_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- PAYMENTS TABLE
-- Tracks payments made to suppliers for specific invoices.
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('BANK_TRANSFER', 'CHEQUE', 'CREDIT_CARD', 'CASH') DEFAULT 'BANK_TRANSFER',
    transaction_ref VARCHAR(255) DEFAULT NULL, -- e.g., Cheque number, bank transaction ID
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- DEFAULT DATA SEEDING

INSERT INTO roles (role_name, description) VALUES
('ADMIN', 'System administrator with full privileges'),
('INVENTORY_MANAGER', 'Responsible for managing inventory and stock'),
('REQUESTER', 'Employee who requests materials or items');

INSERT INTO users (username, password, role_id, status)
VALUES ('root_admin', 'placeholder_hashed_pw', 1, 'ACTIVE');
