# 📊 Database Features & SQL Queries Guide

## Overview

The Food Delivery System now includes a comprehensive database structure with **customers**, **delivery staff**, and enhanced **order tracking**. This document explains the database schema, relationships, and provides SQL query examples for reports and analytics.

---

## 🗄️ Database Schema

### Tables Overview

1. **customers** - Customer information
2. **restaurants** - Restaurant details
3. **menu_items** - Menu items for each restaurant
4. **delivery_staff** - Delivery personnel information
5. **orders** - Order records with customer and delivery staff links
6. **order_items** - Individual items in each order

### Table Relationships

```
customers (1) ────< (many) orders
restaurants (1) ────< (many) orders
delivery_staff (1) ────< (many) orders
orders (1) ────< (many) order_items
menu_items (1) ────< (many) order_items
restaurants (1) ────< (many) menu_items
```

---

## 📋 Table Structures

### 1. Customers Table

```sql
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data**: 8 customers with various locations

### 2. Delivery Staff Table

```sql
CREATE TABLE delivery_staff (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Available',
    rating FLOAT DEFAULT 5.0,
    total_deliveries INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data**: 6 delivery staff members with different vehicle types

### 3. Orders Table (Enhanced)

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    delivery_staff_id INT,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    delivery_address TEXT,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (delivery_staff_id) REFERENCES delivery_staff(id)
);
```

**Key Features**:
- Links to customer who placed the order
- Links to restaurant
- Optional link to assigned delivery staff
- Tracks delivery address and payment method

---

## 🔍 SQL Query Examples

### Basic SELECT Queries

#### Get All Customers
```sql
SELECT * FROM customers;
```

#### Get Available Delivery Staff
```sql
SELECT * FROM delivery_staff WHERE status = 'Available';
```

#### Get Orders by Status
```sql
SELECT * FROM orders WHERE status = 'Pending';
```

### WHERE Clause Examples

#### Find Customers in a Specific City
```sql
SELECT * FROM customers WHERE city = 'New York';
```

#### Get High-Rated Restaurants
```sql
SELECT name, cuisine, rating 
FROM restaurants 
WHERE rating > 4.5;
```

#### Find Orders in Price Range
```sql
SELECT * FROM orders 
WHERE total_price BETWEEN 20.00 AND 50.00;
```

### GROUP BY Queries

#### Count Orders by Status
```sql
SELECT status, COUNT(*) as order_count 
FROM orders 
GROUP BY status;
```

#### Total Revenue by Restaurant
```sql
SELECT 
    r.name as restaurant_name,
    SUM(o.total_price) as total_revenue,
    COUNT(o.id) as order_count
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.id
GROUP BY r.id, r.name
ORDER BY total_revenue DESC;
```

#### Average Order Value by Customer
```sql
SELECT 
    c.name as customer_name,
    AVG(o.total_price) as avg_order_value,
    COUNT(o.id) as total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY avg_order_value DESC;
```

### ORDER BY Examples

#### Restaurants Sorted by Rating
```sql
SELECT name, cuisine, rating 
FROM restaurants 
ORDER BY rating DESC;
```

#### Orders by Total Price (Highest First)
```sql
SELECT id, customer_id, total_price, status 
FROM orders 
ORDER BY total_price DESC;
```

#### Recent Orders
```sql
SELECT * FROM orders 
ORDER BY created_at DESC;
```

### JOIN Queries

#### Orders with Customer and Restaurant Details
```sql
SELECT 
    o.id as order_id,
    c.name as customer_name,
    r.name as restaurant_name,
    o.total_price,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN restaurants r ON o.restaurant_id = r.id
ORDER BY o.created_at DESC;
```

#### Order Details with Items
```sql
SELECT 
    o.id as order_id,
    mi.name as item_name,
    oi.quantity,
    oi.price as item_price
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN menu_items mi ON oi.menu_item_id = mi.id
WHERE o.id = 1;
```

#### Orders with Delivery Staff
```sql
SELECT 
    o.id as order_id,
    c.name as customer_name,
    ds.name as delivery_person,
    ds.vehicle_type,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN delivery_staff ds ON o.delivery_staff_id = ds.id;
```

### Complex Analytics Queries

#### Top 5 Customers by Spending
```sql
SELECT 
    c.name as customer_name,
    COUNT(o.id) as order_count,
    SUM(o.total_price) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 5;
```

#### Restaurant Performance Report
```sql
SELECT 
    r.name as restaurant_name,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_price) as total_revenue,
    AVG(o.total_price) as avg_order_value
FROM restaurants r
LEFT JOIN orders o ON r.id = o.restaurant_id
GROUP BY r.id, r.name
ORDER BY total_revenue DESC;
```

#### Daily Sales Report
```sql
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as order_count,
    SUM(total_price) as daily_revenue
FROM orders
GROUP BY DATE(created_at)
ORDER BY order_date DESC;
```

---

## 🔌 API Endpoints

### Customers

- `GET /api/customers` - Get all customers
- `GET /api/customers/:id` - Get specific customer
- `POST /api/customers` - Create new customer

### Delivery Staff

- `GET /api/delivery-staff` - Get all delivery staff
- `GET /api/delivery-staff?status=Available` - Filter by status
- `GET /api/delivery-staff/:id` - Get specific staff member
- `GET /api/delivery-staff/available` - Get available staff

### Reports & Analytics

- `GET /api/reports/summary` - Overall statistics
- `GET /api/reports/orders-by-status` - Order count by status
- `GET /api/reports/restaurant-revenue` - Revenue by restaurant
- `GET /api/reports/top-customers?limit=5` - Top customers

### Enhanced Orders

- `GET /api/orders` - Now includes customer and delivery staff info
- `POST /api/orders` - Now accepts `customer_id`, `delivery_address`, `payment_method`

---

## 📝 Using SQL Queries

### Running Queries in phpMyAdmin

1. Open phpMyAdmin: `http://localhost/phpmyadmin`
2. Select `food_delivery` database
3. Click on "SQL" tab
4. Paste your query
5. Click "Go" to execute

### Running Queries via MySQL CLI

```bash
mysql -u root -p food_delivery < backend/sql_queries.sql
```

Or interactively:
```bash
mysql -u root -p
USE food_delivery;
SELECT * FROM customers;
```

---

## 🎯 Common Use Cases

### 1. Find Customer Order History
```sql
SELECT 
    c.name,
    o.id as order_id,
    r.name as restaurant,
    o.total_price,
    o.status
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN restaurants r ON o.restaurant_id = r.id
WHERE c.id = 1
ORDER BY o.created_at DESC;
```

### 2. Assign Delivery Staff to Order
```sql
-- Find available delivery staff
SELECT * FROM delivery_staff 
WHERE status = 'Available' 
ORDER BY rating DESC;

-- Update order with delivery staff
UPDATE orders 
SET delivery_staff_id = 1 
WHERE id = 1;
```

### 3. Calculate Monthly Revenue
```sql
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') as month,
    SUM(total_price) as monthly_revenue,
    COUNT(*) as order_count
FROM orders
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month DESC;
```

### 4. Most Popular Menu Items
```sql
SELECT 
    mi.name,
    mi.category,
    SUM(oi.quantity) as total_ordered
FROM menu_items mi
JOIN order_items oi ON mi.id = oi.menu_item_id
GROUP BY mi.id, mi.name, mi.category
ORDER BY total_ordered DESC
LIMIT 10;
```

---

## 📊 Sample Reports

All SQL queries are available in `backend/sql_queries.sql` file, organized by category:

1. **Basic SELECT Queries** - Simple data retrieval
2. **WHERE Conditions** - Filtering data
3. **GROUP BY** - Aggregations
4. **ORDER BY** - Sorting results
5. **JOIN Queries** - Combining tables
6. **Complex Queries** - Advanced analytics
7. **Search & Filter** - Finding specific data
8. **Summary Statistics** - Overall metrics

---

## 🔄 Database Migration

If you have an existing database, you'll need to:

1. **Add new tables**:
   ```sql
   -- Run the CREATE TABLE statements for customers and delivery_staff
   ```

2. **Update orders table**:
   ```sql
   ALTER TABLE orders 
   ADD COLUMN customer_id INT,
   ADD COLUMN delivery_staff_id INT,
   ADD COLUMN delivery_address TEXT,
   ADD COLUMN payment_method VARCHAR(50);
   
   ALTER TABLE orders
   ADD FOREIGN KEY (customer_id) REFERENCES customers(id),
   ADD FOREIGN KEY (delivery_staff_id) REFERENCES delivery_staff(id);
   ```

3. **Insert sample data**:
   ```sql
   -- Run the INSERT statements from database.sql
   ```

---

## ✅ Features Summary

✅ **Customers Management** - Track customer information and order history  
✅ **Delivery Staff** - Manage delivery personnel and assignments  
✅ **Enhanced Orders** - Link orders to customers and delivery staff  
✅ **SQL Queries** - Comprehensive query examples for reports  
✅ **API Endpoints** - RESTful APIs for all entities  
✅ **Analytics** - Built-in reporting endpoints  

---

For more details, see `backend/sql_queries.sql` for complete SQL examples!

