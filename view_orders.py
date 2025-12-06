import sqlite3

conn = sqlite3.connect('backend/food_delivery.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 80)
print("ALL ORDERS IN DATABASE")
print("=" * 80)
print()

# Get all orders with basic info
cursor.execute("""
    SELECT o.id, o.restaurant_id, o.total_price, o.status, o.created_at, r.name as restaurant_name
    FROM orders o
    LEFT JOIN restaurants r ON o.restaurant_id = r.id
    ORDER BY o.id DESC
""")

orders = cursor.fetchall()
if not orders:
    print("No orders found in database")
else:
    for order in orders:
        order_dict = dict(order)
        print(f"Order #{order_dict['id']}")
        print(f"  Restaurant: {order_dict['restaurant_name']}")
        print(f"  Total Price: Rs {order_dict['total_price']}")
        print(f"  Status: {order_dict['status']}")
        print(f"  Created: {order_dict['created_at']}")
        
        # Get items in this order
        cursor.execute("""
            SELECT oi.id, oi.quantity, oi.price, mi.name
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = ?
        """, (order_dict['id'],))
        
        items = cursor.fetchall()
        if items:
            print(f"  Items:")
            for item in items:
                item_dict = dict(item)
                subtotal = item_dict['price'] * item_dict['quantity']
                print(f"    - {item_dict['name']} x{item_dict['quantity']} @ Rs {item_dict['price']} = Rs {subtotal}")
        else:
            print(f"  Items: None")
        print()

print("=" * 80)
print("DIRECT TABLE QUERIES")
print("=" * 80)
print()

print("ORDERS table:")
print("-" * 80)
cursor.execute("SELECT * FROM orders")
for row in cursor.fetchall():
    print(dict(row))
print()

print("ORDER_ITEMS table:")
print("-" * 80)
cursor.execute("SELECT * FROM order_items")
for row in cursor.fetchall():
    print(dict(row))
print()

print("MENU_ITEMS table (sample):")
print("-" * 80)
cursor.execute("SELECT id, name, price FROM menu_items LIMIT 5")
for row in cursor.fetchall():
    print(dict(row))

conn.close()
