CREATE DATABASE ims_db;
USE ims_db;

-- ROLES & USERS

CREATE TABLE roles (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(100) NOT NULL
);

CREATE TABLE users (
  user_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  username VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role_id INT,
  status VARCHAR(50) DEFAULT 'Active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- CATEGORIES & PRODUCTS

CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL
);

CREATE TABLE products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  quantity INT DEFAULT 0,
  category_id INT,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- WAREHOUSES & INVENTORY

CREATE TABLE warehouses (
  warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
  location VARCHAR(255)
);

CREATE TABLE inventory (
  inventory_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT,
  warehouse_id INT,
  stock_level INT DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- SUPPLIERS & PURCHASE ORDERS


CREATE TABLE suppliers (
  supplier_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  contact_info VARCHAR(255)
);

CREATE TABLE purchase_orders (
  purchase_order_id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_id INT,
  date DATETIME,
  status VARCHAR(100),
  FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- CUSTOMERS & ORDERS


CREATE TABLE customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150),
  phone VARCHAR(50)
);

CREATE TABLE orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  date DATETIME,
  status VARCHAR(100),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
  order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  price DECIMAL(10,2),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);


-- INVOICES & PAYMENTS


CREATE TABLE invoices (
  invoice_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT,
  total DECIMAL(10,2),
  date DATETIME,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE payments (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  invoice_id INT,
  method VARCHAR(100),
  amount DECIMAL(10,2),
  FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);


-- REPORTS, NOTIFICATIONS, AUDIT LOGS


CREATE TABLE reports (
  report_id INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(100),
  date DATETIME
);

CREATE TABLE notifications (
  notification_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(50),
  message TEXT,
  date DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE audit_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(50),
  action TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- INSERT DEFAULT ROLES AND ROOT ADMIN


INSERT INTO roles (role_name) VALUES ('Admin'), ('Manager'), ('Cashier');

INSERT INTO users (user_id, name, username, password, role_id)
VALUES ('ADMIN', 'System Admin', 'root_admin', 'PASS0', 1);
