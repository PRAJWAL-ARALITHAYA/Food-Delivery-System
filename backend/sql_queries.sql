-- =====================================================
-- SQL QUERIES FOR FOOD DELIVERY SYSTEM REPORTS
-- =====================================================
-- This file contains various SQL queries demonstrating
-- SELECT, WHERE, GROUP BY, ORDER BY, JOINs, and aggregations
-- =====================================================

-- =====================================================
-- 1. BASIC SELECT QUERIES
-- =====================================================

-- Get all customers
SELECT * FROM customers;

-- Get all restaurants with their cuisine type
SELECT id, name, cuisine, rating FROM restaurants;

-- Get all delivery staff who are available
SELECT * FROM delivery_staff WHERE status = 'Available';

-- Get orders with status 'Pending'
SELECT * FROM orders WHERE status = 'Pending';

-- =====================================================
-- 2. SELECT WITH WHERE CONDITIONS
-- =====================================================

-- Find customers from a specific city
SELECT * FROM customers WHERE city = 'New York';

-- Get restaurants with rating above 4.5
SELECT name, cuisine, rating FROM restaurants WHERE rating > 4.5;

-- Get menu items with price less than $10
SELECT name, price, category FROM menu_items WHERE price < 10.00;

-- Get orders with total price greater than $50
SELECT id, customer_id, total_price, status FROM orders WHERE total_price > 50.00;

-- Get delivery staff with rating above 4.7
SELECT name, phone, vehicle_type, rating FROM delivery_staff WHERE rating > 4.7;

-- Get orders created in the last 7 days
SELECT * FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);

-- =====================================================
-- 3. GROUP BY QUERIES (Aggregations)
-- =====================================================

-- Count orders by status
SELECT status, COUNT(*) as order_count 
FROM orders 
GROUP BY status;

-- Total revenue by restaurant
SELECT 
    r.name as restaurant_name,
    SUM(o.total_price) as total_revenue,
    COUNT(o.id) as order_count
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.id
GROUP BY r.id, r.name
ORDER BY total_revenue DESC;

-- Average order value by customer
SELECT 
    c.name as customer_name,
    AVG(o.total_price) as avg_order_value,
    COUNT(o.id) as total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY avg_order_value DESC;

-- Number of deliveries by delivery staff
SELECT 
    ds.name as delivery_person,
    COUNT(o.id) as deliveries_completed,
    AVG(ds.rating) as avg_rating
FROM delivery_staff ds
LEFT JOIN orders o ON ds.id = o.delivery_staff_id
GROUP BY ds.id, ds.name
ORDER BY deliveries_completed DESC;

-- Menu items count by category
SELECT 
    category,
    COUNT(*) as item_count,
    AVG(price) as avg_price
FROM menu_items
GROUP BY category
ORDER BY item_count DESC;

-- Orders by payment method
SELECT 
    payment_method,
    COUNT(*) as order_count,
    SUM(total_price) as total_amount
FROM orders
WHERE payment_method IS NOT NULL
GROUP BY payment_method;

-- =====================================================
-- 4. ORDER BY QUERIES (Sorting)
-- =====================================================

-- Restaurants sorted by rating (highest first)
SELECT name, cuisine, rating FROM restaurants ORDER BY rating DESC;

-- Menu items sorted by price (lowest first)
SELECT name, price, category FROM menu_items ORDER BY price ASC;

-- Orders sorted by total price (highest first)
SELECT id, customer_id, total_price, status, created_at 
FROM orders 
ORDER BY total_price DESC;

-- Customers sorted by name alphabetically
SELECT name, email, city FROM customers ORDER BY name ASC;

-- Delivery staff sorted by total deliveries
SELECT name, total_deliveries, rating FROM delivery_staff ORDER BY total_deliveries DESC;

-- Recent orders (newest first)
SELECT id, customer_id, total_price, status, created_at 
FROM orders 
ORDER BY created_at DESC;

-- =====================================================
-- 5. JOIN QUERIES (Relationships)
-- =====================================================

-- Get orders with customer and restaurant details
SELECT 
    o.id as order_id,
    c.name as customer_name,
    r.name as restaurant_name,
    o.total_price,
    o.status,
    o.created_at
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN restaurants r ON o.restaurant_id = r.id
ORDER BY o.created_at DESC;

-- Get order details with items
SELECT 
    o.id as order_id,
    o.total_price,
    o.status,
    mi.name as item_name,
    oi.quantity,
    oi.price as item_price,
    (oi.quantity * oi.price) as line_total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN menu_items mi ON oi.menu_item_id = mi.id
ORDER BY o.id, mi.name;

-- Get orders with delivery staff information
SELECT 
    o.id as order_id,
    c.name as customer_name,
    r.name as restaurant_name,
    ds.name as delivery_person,
    ds.vehicle_type,
    o.status,
    o.total_price
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN restaurants r ON o.restaurant_id = r.id
LEFT JOIN delivery_staff ds ON o.delivery_staff_id = ds.id
ORDER BY o.created_at DESC;

-- Get customer order history
SELECT 
    c.name as customer_name,
    c.email,
    o.id as order_id,
    r.name as restaurant_name,
    o.total_price,
    o.status,
    o.created_at
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN restaurants r ON o.restaurant_id = r.id
WHERE c.id = 1  -- Replace with specific customer ID
ORDER BY o.created_at DESC;

-- =====================================================
-- 6. COMPLEX QUERIES (Multiple Conditions)
-- =====================================================

-- Top 5 customers by total spending
SELECT 
    c.name as customer_name,
    c.email,
    COUNT(o.id) as order_count,
    SUM(o.total_price) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY total_spent DESC
LIMIT 5;

-- Most popular menu items (by quantity ordered)
SELECT 
    mi.name as item_name,
    mi.category,
    SUM(oi.quantity) as total_ordered,
    SUM(oi.quantity * oi.price) as total_revenue
FROM menu_items mi
JOIN order_items oi ON mi.id = oi.menu_item_id
GROUP BY mi.id, mi.name, mi.category
ORDER BY total_ordered DESC
LIMIT 10;

-- Restaurant performance report
SELECT 
    r.name as restaurant_name,
    r.cuisine,
    r.rating,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_price) as total_revenue,
    AVG(o.total_price) as avg_order_value
FROM restaurants r
LEFT JOIN orders o ON r.id = o.restaurant_id
GROUP BY r.id, r.name, r.cuisine, r.rating
ORDER BY total_revenue DESC;

-- Delivery staff performance
SELECT 
    ds.name as delivery_person,
    ds.vehicle_type,
    ds.rating,
    COUNT(o.id) as deliveries_completed,
    AVG(TIMESTAMPDIFF(MINUTE, o.created_at, o.updated_at)) as avg_delivery_time_minutes
FROM delivery_staff ds
LEFT JOIN orders o ON ds.id = o.delivery_staff_id AND o.status = 'Delivered'
GROUP BY ds.id, ds.name, ds.vehicle_type, ds.rating
ORDER BY deliveries_completed DESC;

-- Orders by city
SELECT 
    c.city,
    COUNT(o.id) as order_count,
    SUM(o.total_price) as total_revenue,
    AVG(o.total_price) as avg_order_value
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;

-- =====================================================
-- 7. ANALYTICAL QUERIES
-- =====================================================

-- Daily sales report
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as order_count,
    SUM(total_price) as daily_revenue,
    AVG(total_price) as avg_order_value
FROM orders
GROUP BY DATE(created_at)
ORDER BY order_date DESC;

-- Monthly revenue by restaurant
SELECT 
    r.name as restaurant_name,
    DATE_FORMAT(o.created_at, '%Y-%m') as month,
    COUNT(o.id) as order_count,
    SUM(o.total_price) as monthly_revenue
FROM restaurants r
JOIN orders o ON r.id = o.restaurant_id
GROUP BY r.id, r.name, DATE_FORMAT(o.created_at, '%Y-%m')
ORDER BY month DESC, monthly_revenue DESC;

-- Customer lifetime value
SELECT 
    c.id,
    c.name,
    c.email,
    COUNT(DISTINCT o.id) as total_orders,
    SUM(o.total_price) as lifetime_value,
    AVG(o.total_price) as avg_order_value,
    MIN(o.created_at) as first_order_date,
    MAX(o.created_at) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY lifetime_value DESC;

-- Order status distribution
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY status
ORDER BY count DESC;

-- =====================================================
-- 8. SEARCH AND FILTER QUERIES
-- =====================================================

-- Search customers by name or email
SELECT * FROM customers 
WHERE name LIKE '%John%' OR email LIKE '%john%';

-- Find orders in a price range
SELECT * FROM orders 
WHERE total_price BETWEEN 20.00 AND 50.00
ORDER BY total_price;

-- Get available delivery staff for assignment
SELECT * FROM delivery_staff 
WHERE status = 'Available' 
ORDER BY rating DESC, total_deliveries ASC;

-- Get pending orders that need delivery staff
SELECT 
    o.id,
    c.name as customer_name,
    r.name as restaurant_name,
    o.total_price,
    o.delivery_address
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN restaurants r ON o.restaurant_id = r.id
WHERE o.status = 'Out for Delivery' AND o.delivery_staff_id IS NULL;

-- =====================================================
-- 9. SUMMARY STATISTICS
-- =====================================================

-- Overall system statistics
SELECT 
    (SELECT COUNT(*) FROM customers) as total_customers,
    (SELECT COUNT(*) FROM restaurants) as total_restaurants,
    (SELECT COUNT(*) FROM delivery_staff) as total_delivery_staff,
    (SELECT COUNT(*) FROM orders) as total_orders,
    (SELECT SUM(total_price) FROM orders) as total_revenue,
    (SELECT AVG(total_price) FROM orders) as avg_order_value;

-- Restaurant statistics
SELECT 
    COUNT(*) as total_restaurants,
    AVG(rating) as avg_rating,
    MIN(delivery_time) as fastest_delivery,
    MAX(delivery_time) as slowest_delivery
FROM restaurants;

-- =====================================================
-- END OF SQL QUERIES
-- =====================================================

