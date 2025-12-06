-- Migration Script to Add Customers and Delivery Staff Features
-- Run this if you have an existing database and want to add the new features
-- WITHOUT losing existing data

USE food_delivery;

-- Step 1: Create customers table if it doesn't exist
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Create delivery_staff table if it doesn't exist
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

-- Step 3: Ensure customers table has at least one customer before adding foreign keys
-- Insert a default customer if customers table is empty
INSERT INTO customers (id, name, email, phone, address, city)
SELECT 1, 'Default Customer', 'customer@fooddelivery.com', '+1-555-0000', 'Default Address', 'Default City'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE id = 1);

-- Step 4: Add new columns to orders table (if they don't exist)
-- First, add customer_id column WITHOUT foreign key
SET @dbname = DATABASE();
SET @tablename = "orders";
SET @columnname = "customer_id";

-- Check if column exists
SET @columnExists = (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE table_name = @tablename
    AND table_schema = @dbname
    AND column_name = @columnname
);

-- Add column if it doesn't exist
SET @preparedStatement = IF(@columnExists = 0,
  CONCAT("ALTER TABLE ", @tablename, " ADD COLUMN ", @columnname, " INT DEFAULT 1"),
  "SELECT 'Column customer_id already exists.' AS message"
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Update all existing orders to have customer_id = 1
UPDATE orders SET customer_id = 1 WHERE customer_id IS NULL OR customer_id NOT IN (SELECT id FROM customers);

-- Now add foreign key constraint (check if it doesn't exist first)
SET @fkExists = (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
  WHERE table_schema = @dbname
    AND table_name = @tablename
    AND column_name = @columnname
    AND referenced_table_name = 'customers'
);

SET @preparedStatement = IF(@fkExists = 0,
  CONCAT("ALTER TABLE ", @tablename, " ADD FOREIGN KEY (", @columnname, ") REFERENCES customers(id) ON DELETE CASCADE"),
  "SELECT 'Foreign key already exists.' AS message"
);
PREPARE addFK FROM @preparedStatement;
EXECUTE addFK;
DEALLOCATE PREPARE addFK;

-- Add delivery_staff_id column (without foreign key first)
SET @columnname = "delivery_staff_id";
SET @columnExists = (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE table_name = @tablename
    AND table_schema = @dbname
    AND column_name = @columnname
);

SET @preparedStatement = IF(@columnExists = 0,
  CONCAT("ALTER TABLE ", @tablename, " ADD COLUMN ", @columnname, " INT"),
  "SELECT 'Column delivery_staff_id already exists.' AS message"
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Add foreign key for delivery_staff_id (if it doesn't exist)
SET @fkExists = (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
  WHERE table_schema = @dbname
    AND table_name = @tablename
    AND column_name = @columnname
    AND referenced_table_name = 'delivery_staff'
);

SET @preparedStatement = IF(@fkExists = 0,
  CONCAT("ALTER TABLE ", @tablename, " ADD FOREIGN KEY (", @columnname, ") REFERENCES delivery_staff(id) ON DELETE SET NULL"),
  "SELECT 'Foreign key already exists.' AS message"
);
PREPARE addFK FROM @preparedStatement;
EXECUTE addFK;
DEALLOCATE PREPARE addFK;

-- Check and add delivery_address
SET @columnname = "delivery_address";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 'Column already exists.'",
  CONCAT("ALTER TABLE ", @tablename, " ADD COLUMN ", @columnname, " TEXT")
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Check and add payment_method
SET @columnname = "payment_method";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 'Column already exists.'",
  CONCAT("ALTER TABLE ", @tablename, " ADD COLUMN ", @columnname, " VARCHAR(50)")
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Step 5: Insert sample data (only if tables are empty or need more data)
-- Insert additional customers if table has only the default customer
INSERT INTO customers (name, email, phone, address, city)
SELECT 'John Smith', 'john.smith@email.com', '+1-555-0101', '123 Main Street, Apt 4B', 'New York'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE email = 'john.smith@email.com');

INSERT INTO customers (name, email, phone, address, city)
SELECT 'Sarah Johnson', 'sarah.j@email.com', '+1-555-0102', '456 Oak Avenue', 'Los Angeles'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE email = 'sarah.j@email.com');

INSERT INTO customers (name, email, phone, address, city)
SELECT 'Michael Brown', 'michael.brown@email.com', '+1-555-0103', '789 Pine Road', 'Chicago'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE email = 'michael.brown@email.com');

-- Insert delivery staff if table is empty
INSERT INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries)
SELECT 'James Rodriguez', '+1-555-0201', 'Motorcycle', 'Available', 4.8, 245
WHERE NOT EXISTS (SELECT 1 FROM delivery_staff WHERE phone = '+1-555-0201');

INSERT INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries)
SELECT 'Maria Garcia', '+1-555-0202', 'Bicycle', 'Available', 4.9, 312
WHERE NOT EXISTS (SELECT 1 FROM delivery_staff WHERE phone = '+1-555-0202');

INSERT INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries)
SELECT 'Thomas Lee', '+1-555-0203', 'Car', 'Available', 4.7, 189
WHERE NOT EXISTS (SELECT 1 FROM delivery_staff WHERE phone = '+1-555-0203');

SELECT 'Migration completed successfully!' AS status;

