#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = 'backend/food_delivery.db'

# SQL statements for creating tables
sql_statements = [
    """CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cuisine TEXT,
        rating REAL DEFAULT 4.0,
        delivery_time INTEGER,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    
    """CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        image_url TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
    )""",
    
    """CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
    )""",
    
    """CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        menu_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        price DECIMAL(10, 2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
    )"""
]

# Sample data
restaurants_data = [
    ('Pizza Palace', 'Italian', 4.5, 30, 'https://via.placeholder.com/200?text=Pizza+Palace'),
    ('Burger Bistro', 'American', 4.2, 25, 'https://via.placeholder.com/200?text=Burger+Bistro'),
    ('Sushi Supreme', 'Japanese', 4.8, 40, 'https://via.placeholder.com/200?text=Sushi+Supreme'),
    ('Taco Fiesta', 'Mexican', 4.3, 20, 'https://via.placeholder.com/200?text=Taco+Fiesta'),
    ('Curry House', 'Indian', 4.6, 35, 'https://via.placeholder.com/200?text=Curry+House'),
]

menu_data = [
    # Pizza Palace
    (1, 'Margherita Pizza', 'Classic pizza with tomato, mozzarella, and basil', 8.99, 'https://via.placeholder.com/150?text=Margherita', 'Pizza'),
    (1, 'Pepperoni Pizza', 'Traditional pepperoni pizza', 10.99, 'https://via.placeholder.com/150?text=Pepperoni', 'Pizza'),
    (1, 'Garlic Bread', 'Crispy garlic bread', 3.99, 'https://via.placeholder.com/150?text=Garlic+Bread', 'Appetizer'),
    (1, 'Caesar Salad', 'Fresh caesar salad', 5.99, 'https://via.placeholder.com/150?text=Caesar+Salad', 'Salad'),
    # Burger Bistro
    (2, 'Classic Burger', 'Juicy burger with cheese and lettuce', 9.99, 'https://via.placeholder.com/150?text=Classic+Burger', 'Burger'),
    (2, 'Double Cheeseburger', 'Two patties with double cheese', 12.99, 'https://via.placeholder.com/150?text=Double+Cheeseburger', 'Burger'),
    (2, 'French Fries', 'Crispy french fries', 3.49, 'https://via.placeholder.com/150?text=Fries', 'Sides'),
    (2, 'Milkshake', 'Vanilla milkshake', 4.99, 'https://via.placeholder.com/150?text=Milkshake', 'Beverage'),
    # Sushi Supreme
    (3, 'California Roll', 'Crab, avocado, cucumber', 12.99, 'https://via.placeholder.com/150?text=California+Roll', 'Sushi'),
    (3, 'Spicy Tuna Roll', 'Spicy tuna with mayo', 14.99, 'https://via.placeholder.com/150?text=Spicy+Tuna', 'Sushi'),
    (3, 'Salmon Sashimi', 'Fresh salmon sashimi', 16.99, 'https://via.placeholder.com/150?text=Salmon+Sashimi', 'Sashimi'),
    (3, 'Miso Soup', 'Traditional miso soup', 3.99, 'https://via.placeholder.com/150?text=Miso+Soup', 'Soup'),
    # Taco Fiesta
    (4, 'Beef Tacos', 'Three soft beef tacos', 8.99, 'https://via.placeholder.com/150?text=Beef+Tacos', 'Tacos'),
    (4, 'Chicken Enchiladas', 'Three chicken enchiladas', 11.99, 'https://via.placeholder.com/150?text=Enchiladas', 'Entree'),
    (4, 'Guacamole Dip', 'Fresh guacamole with chips', 6.99, 'https://via.placeholder.com/150?text=Guacamole', 'Appetizer'),
    (4, 'Churros', 'Fried churros with chocolate', 5.99, 'https://via.placeholder.com/150?text=Churros', 'Dessert'),
    # Curry House
    (5, 'Butter Chicken', 'Creamy butter chicken curry', 13.99, 'https://via.placeholder.com/150?text=Butter+Chicken', 'Curry'),
    (5, 'Tandoori Chicken', 'Marinated tandoori chicken', 14.99, 'https://via.placeholder.com/150?text=Tandoori', 'Grill'),
    (5, 'Naan Bread', 'Freshly baked naan', 2.99, 'https://via.placeholder.com/150?text=Naan', 'Bread'),
    (5, 'Mango Lassi', 'Refreshing mango lassi', 3.99, 'https://via.placeholder.com/150?text=Lassi', 'Beverage'),
]

try:
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    for statement in sql_statements:
        cursor.execute(statement)
    
    # Insert restaurants
    cursor.executemany(
        "INSERT INTO restaurants (name, cuisine, rating, delivery_time, image_url) VALUES (?, ?, ?, ?, ?)",
        restaurants_data
    )
    
    # Insert menu items
    cursor.executemany(
        "INSERT INTO menu_items (restaurant_id, name, description, price, image_url, category) VALUES (?, ?, ?, ?, ?, ?)",
        menu_data
    )
    
    conn.commit()
    conn.close()
    
    print("[SUCCESS] Database initialized successfully!")
    print(f"Database created at: {DB_PATH}")
    print("- 5 restaurants added")
    print("- 20 menu items added")
    
except Exception as e:
    print(f"[ERROR] Database initialization failed: {e}")
