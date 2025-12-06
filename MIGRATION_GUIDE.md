# 🔄 Database Migration Guide

## Problem: "Failed to fetch orders" Error

If you're seeing the "Failed to fetch orders" error, it's likely because your database hasn't been updated with the new schema that includes `customers` and `delivery_staff` tables.

## Solution Options

### Option 1: Fresh Database Setup (Recommended if you don't have important data)

1. **Backup existing data** (if needed):
   ```sql
   -- Export your data first if you have important orders
   ```

2. **Drop and recreate database**:
   ```sql
   DROP DATABASE IF EXISTS food_delivery;
   ```

3. **Import the new schema**:
   - Open phpMyAdmin: `http://localhost/phpmyadmin`
   - Click "Import"
   - Select `backend/database.sql`
   - Click "Go"

### Option 2: Migration Script (Keep existing data)

1. **Run the migration script**:
   - Open phpMyAdmin: `http://localhost/phpmyadmin`
   - Select `food_delivery` database
   - Click "SQL" tab
   - Copy and paste contents of `backend/migrate_database.sql`
   - Click "Go"

   OR via command line:
   ```bash
   mysql -u root -p food_delivery < backend/migrate_database.sql
   ```

2. **Verify migration**:
   ```sql
   SHOW TABLES;
   -- Should show: customers, delivery_staff, restaurants, menu_items, orders, order_items
   
   DESCRIBE orders;
   -- Should show: customer_id, delivery_staff_id, delivery_address, payment_method columns
   ```

### Option 3: Manual Migration

If the migration script doesn't work, run these commands manually:

```sql
USE food_delivery;

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create delivery_staff table
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

-- Add columns to orders table
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS customer_id INT DEFAULT 1,
ADD COLUMN IF NOT EXISTS delivery_staff_id INT,
ADD COLUMN IF NOT EXISTS delivery_address TEXT,
ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50);

-- Add foreign keys
ALTER TABLE orders
ADD FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
ADD FOREIGN KEY (delivery_staff_id) REFERENCES delivery_staff(id) ON DELETE SET NULL;

-- Insert sample data
INSERT INTO customers (name, email, phone, address, city) VALUES
('John Smith', 'john.smith@email.com', '+1-555-0101', '123 Main Street, Apt 4B', 'New York'),
('Sarah Johnson', 'sarah.j@email.com', '+1-555-0102', '456 Oak Avenue', 'Los Angeles'),
('Michael Brown', 'michael.brown@email.com', '+1-555-0103', '789 Pine Road', 'Chicago'),
('Emily Davis', 'emily.davis@email.com', '+1-555-0104', '321 Elm Street', 'Houston'),
('David Wilson', 'david.w@email.com', '+1-555-0105', '654 Maple Drive', 'Phoenix');

INSERT INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries) VALUES
('James Rodriguez', '+1-555-0201', 'Motorcycle', 'Available', 4.8, 245),
('Maria Garcia', '+1-555-0202', 'Bicycle', 'Available', 4.9, 312),
('Thomas Lee', '+1-555-0203', 'Car', 'Available', 4.7, 189);

-- Update existing orders to have customer_id
UPDATE orders SET customer_id = 1 WHERE customer_id IS NULL;
```

## Verification Steps

After migration, verify everything works:

1. **Check backend is running**:
   ```bash
   # In backend folder
   python app.py
   ```

2. **Test API endpoint**:
   - Open: `http://localhost:5000/api/orders`
   - Should return JSON (even if empty array `[]`)

3. **Check frontend**:
   - Open: `http://localhost:3000/orders`
   - Should show orders or "No orders found" (not an error)

4. **Test new endpoints**:
   - `http://localhost:5000/api/customers` - Should return customer list
   - `http://localhost:5000/api/delivery-staff` - Should return delivery staff list

## Troubleshooting

### Error: "Table 'customers' doesn't exist"
- Run the migration script or create tables manually

### Error: "Column 'customer_id' doesn't exist"
- Run the ALTER TABLE statements to add columns

### Error: "Foreign key constraint fails"
- Make sure customers and delivery_staff tables exist first
- Make sure you have at least one customer (id=1) before adding foreign key

### Error: "Duplicate entry for key 'email'"
- Customer email must be unique. Change the email in the INSERT statement.

## Need Help?

If migration fails:
1. Check MySQL error messages in phpMyAdmin
2. Verify XAMPP MySQL is running
3. Check backend console for detailed error messages
4. Make sure you're using the correct database name (`food_delivery`)

