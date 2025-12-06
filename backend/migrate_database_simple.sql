-- Simple Migration Script - Run this if the main migration failed
-- This script handles partial migrations and fixes foreign key issues

USE food_delivery;

-- Step 1: Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Create delivery_staff table
CREATE TABLE IF NOT EXISTS delivery_staff (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Available',
    rating FLOAT DEFAULT 5.0,
    total_deliveries INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Insert default customer (id=1) if it doesn't exist
INSERT IGNORE INTO customers (id, name, email, phone, address, city) 
VALUES (1, 'Default Customer', 'customer@fooddelivery.com', '+1-555-0000', 'Default Address', 'Default City');

-- Step 4: Add customer_id column if it doesn't exist
SET @col_exists = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'customer_id'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE orders ADD COLUMN customer_id INT DEFAULT 1',
    'SELECT "Column customer_id already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 5: Update all orders to have valid customer_id
UPDATE orders SET customer_id = 1 WHERE customer_id IS NULL OR customer_id NOT IN (SELECT id FROM customers);

-- Step 6: Remove existing foreign key if it exists (to avoid conflicts)
SET @fk_name = (
    SELECT CONSTRAINT_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'customer_id' 
      AND REFERENCED_TABLE_NAME = 'customers'
    LIMIT 1
);

SET @sql = IF(@fk_name IS NOT NULL, 
    CONCAT('ALTER TABLE orders DROP FOREIGN KEY ', @fk_name), 
    'SELECT "No foreign key to drop" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 7: Add foreign key constraint
ALTER TABLE orders 
ADD CONSTRAINT fk_orders_customer 
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE;

-- Step 8: Add delivery_staff_id column if it doesn't exist
SET @col_exists2 = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'delivery_staff_id'
);

SET @sql3 = IF(@col_exists2 = 0,
    'ALTER TABLE orders ADD COLUMN delivery_staff_id INT',
    'SELECT "Column delivery_staff_id already exists" AS message'
);

PREPARE stmt3 FROM @sql3;
EXECUTE stmt3;
DEALLOCATE PREPARE stmt3;

-- Step 9: Remove existing foreign key for delivery_staff if it exists
SET @fk_name2 = (
    SELECT CONSTRAINT_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'delivery_staff_id' 
      AND REFERENCED_TABLE_NAME = 'delivery_staff'
    LIMIT 1
);

SET @sql2 = IF(@fk_name2 IS NOT NULL, 
    CONCAT('ALTER TABLE orders DROP FOREIGN KEY ', @fk_name2), 
    'SELECT "No foreign key to drop" AS message'
);

PREPARE stmt2 FROM @sql2;
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;

-- Step 10: Add foreign key for delivery_staff
ALTER TABLE orders 
ADD CONSTRAINT fk_orders_delivery_staff 
FOREIGN KEY (delivery_staff_id) REFERENCES delivery_staff(id) ON DELETE SET NULL;

-- Step 11: Add other columns if they don't exist
SET @col_exists3 = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'delivery_address'
);

SET @sql4 = IF(@col_exists3 = 0,
    'ALTER TABLE orders ADD COLUMN delivery_address TEXT',
    'SELECT "Column delivery_address already exists" AS message'
);

PREPARE stmt4 FROM @sql4;
EXECUTE stmt4;
DEALLOCATE PREPARE stmt4;

SET @col_exists4 = (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'orders' 
      AND COLUMN_NAME = 'payment_method'
);

SET @sql5 = IF(@col_exists4 = 0,
    'ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50)',
    'SELECT "Column payment_method already exists" AS message'
);

PREPARE stmt5 FROM @sql5;
EXECUTE stmt5;
DEALLOCATE PREPARE stmt5;

-- Step 12: Insert sample data
INSERT IGNORE INTO customers (name, email, phone, address, city) VALUES
('John Smith', 'john.smith@email.com', '+1-555-0101', '123 Main Street, Apt 4B', 'New York'),
('Sarah Johnson', 'sarah.j@email.com', '+1-555-0102', '456 Oak Avenue', 'Los Angeles'),
('Michael Brown', 'michael.brown@email.com', '+1-555-0103', '789 Pine Road', 'Chicago');

INSERT IGNORE INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries) VALUES
('James Rodriguez', '+1-555-0201', 'Motorcycle', 'Available', 4.8, 245),
('Maria Garcia', '+1-555-0202', 'Bicycle', 'Available', 4.9, 312),
('Thomas Lee', '+1-555-0203', 'Car', 'Available', 4.7, 189);

SELECT 'Migration completed successfully!' AS status;

