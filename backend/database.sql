-- Create Database
CREATE DATABASE IF NOT EXISTS food_delivery;
USE food_delivery;

-- Restaurants Table
CREATE TABLE IF NOT EXISTS restaurants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(50),
    rating FLOAT DEFAULT 4.0,
    delivery_time INT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Delivery Staff Table
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

-- Orders Table (Updated with customer and delivery staff)
CREATE TABLE IF NOT EXISTS orders (
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
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_staff_id) REFERENCES delivery_staff(id) ON DELETE SET NULL
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Sample Data

-- Customers
INSERT INTO customers (name, email, phone, address, city) VALUES
('John Smith', 'john.smith@email.com', '+1-555-0101', '123 Main Street, Apt 4B', 'New York'),
('Sarah Johnson', 'sarah.j@email.com', '+1-555-0102', '456 Oak Avenue', 'Los Angeles'),
('Michael Brown', 'michael.brown@email.com', '+1-555-0103', '789 Pine Road', 'Chicago'),
('Emily Davis', 'emily.davis@email.com', '+1-555-0104', '321 Elm Street', 'Houston'),
('David Wilson', 'david.w@email.com', '+1-555-0105', '654 Maple Drive', 'Phoenix'),
('Lisa Anderson', 'lisa.a@email.com', '+1-555-0106', '987 Cedar Lane', 'Philadelphia'),
('Robert Taylor', 'robert.t@email.com', '+1-555-0107', '147 Birch Court', 'San Antonio'),
('Jennifer Martinez', 'jennifer.m@email.com', '+1-555-0108', '258 Spruce Way', 'San Diego');

-- Delivery Staff
INSERT INTO delivery_staff (name, phone, vehicle_type, status, rating, total_deliveries) VALUES
('James Rodriguez', '+1-555-0201', 'Motorcycle', 'Available', 4.8, 245),
('Maria Garcia', '+1-555-0202', 'Bicycle', 'Available', 4.9, 312),
('Thomas Lee', '+1-555-0203', 'Car', 'Available', 4.7, 189),
('Patricia White', '+1-555-0204', 'Motorcycle', 'Available', 4.6, 278),
('Christopher Harris', '+1-555-0205', 'Bicycle', 'Busy', 4.8, 156),
('Jessica Clark', '+1-555-0206', 'Car', 'Available', 4.9, 203);

-- Restaurants
INSERT INTO restaurants (name, cuisine, rating, delivery_time, image_url) VALUES
('Pizza Palace', 'Italian', 4.5, 30, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop'),
('Burger Bistro', 'American', 4.2, 25, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop'),
('Sushi Supreme', 'Japanese', 4.8, 40, 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop'),
('Taco Fiesta', 'Mexican', 4.3, 20, 'https://images.unsplash.com/photo-1565299585323-38174c3c6a0a?w=400&h=300&fit=crop'),
('Curry House', 'Indian', 4.6, 35, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop');

-- Pizza Palace Menu
INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url) VALUES
(1, 'Margherita Pizza', 'Classic pizza with tomato, mozzarella, and basil', 8.99, 'Pizza', 'https://via.placeholder.com/150?text=Margherita'),
(1, 'Pepperoni Pizza', 'Traditional pepperoni pizza', 10.99, 'Pizza', 'https://via.placeholder.com/150?text=Pepperoni'),
(1, 'Garlic Bread', 'Crispy garlic bread', 3.99, 'Appetizer', 'https://via.placeholder.com/150?text=Garlic+Bread'),
(1, 'Caesar Salad', 'Fresh caesar salad', 5.99, 'Salad', 'https://via.placeholder.com/150?text=Caesar+Salad');

-- Burger Bistro Menu
INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url) VALUES
(2, 'Classic Burger', 'Juicy burger with cheese and lettuce', 9.99, 'Burger', 'https://via.placeholder.com/150?text=Classic+Burger'),
(2, 'Double Cheeseburger', 'Two patties with double cheese', 12.99, 'Burger', 'https://via.placeholder.com/150?text=Double+Cheeseburger'),
(2, 'French Fries', 'Crispy french fries', 3.49, 'Sides', 'https://via.placeholder.com/150?text=Fries'),
(2, 'Milkshake', 'Vanilla milkshake', 4.99, 'Beverage', 'https://via.placeholder.com/150?text=Milkshake');

-- Sushi Supreme Menu
INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url) VALUES
(3, 'California Roll', 'Crab, avocado, cucumber', 12.99, 'Sushi', 'https://via.placeholder.com/150?text=California+Roll'),
(3, 'Spicy Tuna Roll', 'Spicy tuna with mayo', 14.99, 'Sushi', 'https://via.placeholder.com/150?text=Spicy+Tuna'),
(3, 'Salmon Sashimi', 'Fresh salmon sashimi', 16.99, 'Sashimi', 'https://via.placeholder.com/150?text=Salmon+Sashimi'),
(3, 'Miso Soup', 'Traditional miso soup', 3.99, 'Soup', 'https://via.placeholder.com/150?text=Miso+Soup');

-- Taco Fiesta Menu
INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url) VALUES
(4, 'Beef Tacos', 'Three soft beef tacos', 8.99, 'Tacos', 'https://via.placeholder.com/150?text=Beef+Tacos'),
(4, 'Chicken Enchiladas', 'Three chicken enchiladas', 11.99, 'Entree', 'https://via.placeholder.com/150?text=Enchiladas'),
(4, 'Guacamole Dip', 'Fresh guacamole with chips', 6.99, 'Appetizer', 'https://via.placeholder.com/150?text=Guacamole'),
(4, 'Churros', 'Fried churros with chocolate', 5.99, 'Dessert', 'https://via.placeholder.com/150?text=Churros');

-- Curry House Menu
INSERT INTO menu_items (restaurant_id, name, description, price, category, image_url) VALUES
(5, 'Butter Chicken', 'Creamy butter chicken curry', 13.99, 'Curry', 'https://via.placeholder.com/150?text=Butter+Chicken'),
(5, 'Tandoori Chicken', 'Marinated tandoori chicken', 14.99, 'Grill', 'https://via.placeholder.com/150?text=Tandoori'),
(5, 'Naan Bread', 'Freshly baked naan', 2.99, 'Bread', 'https://via.placeholder.com/150?text=Naan'),
(5, 'Mango Lassi', 'Refreshing mango lassi', 3.99, 'Beverage', 'https://via.placeholder.com/150?text=Lassi');

-- =====================================================
-- STORED PROCEDURES AND TRIGGERS
-- =====================================================

-- Procedure: Assign Delivery Staff to Order
DROP PROCEDURE IF EXISTS assign_delivery_staff_to_order;

DELIMITER $$

CREATE PROCEDURE assign_delivery_staff_to_order (
    IN p_order_id INT
)
BEGIN
    DECLARE v_staff_id INT;
    
    -- Pick best available delivery staff:
    -- highest rating, then lowest total_deliveries
    SELECT id INTO v_staff_id
    FROM delivery_staff
    WHERE status = 'Available'
    ORDER BY rating DESC, total_deliveries ASC
    LIMIT 1;
    
    -- If someone is available, assign them
    IF v_staff_id IS NOT NULL THEN
        UPDATE orders
        SET delivery_staff_id = v_staff_id,
            status = 'Out for Delivery'
        WHERE id = p_order_id;
        
        UPDATE delivery_staff
        SET status = 'Busy',
            total_deliveries = total_deliveries + 1
        WHERE id = v_staff_id;
    END IF;
END$$

DELIMITER ;

-- Trigger: Auto-update Order Total Price when items are added
DROP TRIGGER IF EXISTS trg_order_items_after_insert;

DELIMITER $$

CREATE TRIGGER trg_order_items_after_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_price = (
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END$$

DELIMITER ;

-- Trigger: Auto-update Order Total Price when items are updated
DROP TRIGGER IF EXISTS trg_order_items_after_update;

DELIMITER $$

CREATE TRIGGER trg_order_items_after_update
AFTER UPDATE ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_price = (
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END$$

DELIMITER ;

-- Trigger: Auto-update Order Total Price when items are deleted
DROP TRIGGER IF EXISTS trg_order_items_after_delete;

DELIMITER $$

CREATE TRIGGER trg_order_items_after_delete
AFTER DELETE ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_price = (
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = OLD.order_id
    )
    WHERE id = OLD.order_id;
END$$

DELIMITER ;
