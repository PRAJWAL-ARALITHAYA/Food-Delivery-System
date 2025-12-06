@echo off
REM Simple database viewer script for FoodHub
title FoodHub - Database Viewer
cls

echo.
echo ======================================
echo   FoodHub Database Viewer
echo ======================================
echo.
echo Choose an option:
echo.
echo 1. View all orders
echo 2. View order details
echo 3. View all menu items
echo 4. View restaurants
echo 5. Export orders to CSV
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto view_orders
if "%choice%"=="2" goto view_order_details
if "%choice%"=="3" goto view_menu
if "%choice%"=="4" goto view_restaurants
if "%choice%"=="5" goto export_csv
if "%choice%"=="6" exit /b

echo Invalid choice. Please try again.
pause
cls
goto :EOF

:view_orders
python << PYTHON_SCRIPT
import sqlite3
conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*80)
print("ALL ORDERS")
print("="*80 + "\n")

cursor.execute("""
    SELECT o.id, r.name as restaurant, o.total_price, o.status, o.created_at
    FROM orders o
    LEFT JOIN restaurants r ON o.restaurant_id = r.id
    ORDER BY o.id DESC
""")

rows = cursor.fetchall()
if not rows:
    print("No orders found")
else:
    print(f"{'ID':<5} {'Restaurant':<20} {'Total':<10} {'Status':<15} {'Created':<20}")
    print("-"*80)
    for row in rows:
        r = dict(row)
        print(f"{r['id']:<5} {r['restaurant']:<20} Rs {r['total_price']:<8} {r['status']:<15} {r['created_at']:<20}")

conn.close()
PYTHON_SCRIPT
pause
goto :EOF

:view_order_details
set /p order_id="Enter Order ID: "
python << PYTHON_SCRIPT
import sqlite3
order_id = %order_id%
conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*80)
print(f"ORDER #{order_id} DETAILS")
print("="*80 + "\n")

cursor.execute("""
    SELECT o.id, r.name as restaurant, o.total_price, o.status, o.created_at
    FROM orders o
    LEFT JOIN restaurants r ON o.restaurant_id = r.id
    WHERE o.id = ?
""", (order_id,))

order = cursor.fetchone()
if not order:
    print(f"Order #{order_id} not found")
else:
    o = dict(order)
    print(f"Order ID: {o['id']}")
    print(f"Restaurant: {o['restaurant']}")
    print(f"Status: {o['status']}")
    print(f"Total Price: Rs {o['total_price']}")
    print(f"Created: {o['created_at']}")
    print()
    print("Items in Order:")
    print("-"*80)
    
    cursor.execute("""
        SELECT mi.name, oi.quantity, oi.price, (oi.quantity * oi.price) as subtotal
        FROM order_items oi
        LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = ?
    """, (order_id,))
    
    items = cursor.fetchall()
    print(f"{'Item Name':<30} {'Qty':<5} {'Price':<10} {'Subtotal':<10}")
    print("-"*80)
    for item in items:
        i = dict(item)
        print(f"{i['name']:<30} {i['quantity']:<5} Rs {i['price']:<8} Rs {i['subtotal']:<8}")

conn.close()
PYTHON_SCRIPT
pause
goto :EOF

:view_menu
python << PYTHON_SCRIPT
import sqlite3
conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*80)
print("ALL MENU ITEMS")
print("="*80 + "\n")

cursor.execute("""
    SELECT m.id, m.name, r.name as restaurant, m.category, m.price
    FROM menu_items m
    LEFT JOIN restaurants r ON m.restaurant_id = r.id
    ORDER BY r.name, m.category, m.name
""")

rows = cursor.fetchall()
print(f"{'ID':<5} {'Item Name':<25} {'Restaurant':<20} {'Category':<15} {'Price':<10}")
print("-"*80)
for row in rows:
    m = dict(row)
    print(f"{m['id']:<5} {m['name']:<25} {m['restaurant']:<20} {m['category']:<15} Rs {m['price']:<8}")

conn.close()
PYTHON_SCRIPT
pause
goto :EOF

:view_restaurants
python << PYTHON_SCRIPT
import sqlite3
conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\n" + "="*80)
print("ALL RESTAURANTS")
print("="*80 + "\n")

cursor.execute("SELECT id, name, cuisine, rating, delivery_time FROM restaurants ORDER BY id")

rows = cursor.fetchall()
print(f"{'ID':<5} {'Name':<25} {'Cuisine':<15} {'Rating':<10} {'Delivery (min)':<15}")
print("-"*80)
for row in rows:
    r = dict(row)
    print(f"{r['id']:<5} {r['name']:<25} {r['cuisine']:<15} {r['rating']:<10} {r['delivery_time']:<15}")

conn.close()
PYTHON_SCRIPT
pause
goto :EOF

:export_csv
python << PYTHON_SCRIPT
import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

filename = f"orders_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

cursor.execute("""
    SELECT o.id, r.name as restaurant, o.total_price, o.status, o.created_at
    FROM orders o
    LEFT JOIN restaurants r ON o.restaurant_id = r.id
    ORDER BY o.id
""")

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Order ID', 'Restaurant', 'Total Price', 'Status', 'Created'])
    for row in cursor.fetchall():
        r = dict(row)
        writer.writerow([r['id'], r['restaurant'], r['total_price'], r['status'], r['created_at']])

print(f"\nOrders exported to: {filename}")
conn.close()
PYTHON_SCRIPT
pause
goto :EOF
