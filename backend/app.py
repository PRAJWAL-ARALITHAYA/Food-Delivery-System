from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import os
import mysql.connector
import threading
import time

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration (defaults match XAMPP)
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'food_delivery')

def get_db():
    """Create a new MySQL connection using app config"""
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        auth_plugin='mysql_native_password'
    )

def dict_from_row(row):
    """Ensure rows are returned as plain dictionaries with numeric types converted"""
    if row is None:
        return None
    if isinstance(row, dict):
        result = {}
        for key, value in row.items():
            # Convert DECIMAL/string numbers to float
            if isinstance(value, str) and key in ['price', 'total_price', 'rating']:
                try:
                    result[key] = float(value)
                except (ValueError, TypeError):
                    result[key] = value
            else:
                result[key] = value
        return result
    try:
        row_dict = dict(row)
        # Convert DECIMAL/string numbers to float
        result = {}
        for key, value in row_dict.items():
            if isinstance(value, str) and key in ['price', 'total_price', 'rating']:
                try:
                    result[key] = float(value)
                except (ValueError, TypeError):
                    result[key] = value
            else:
                result[key] = value
        return result
    except Exception:
        return row

# ==================== RESTAURANTS ====================

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """Get all restaurants"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM restaurants")
        restaurants = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    """Get specific restaurant"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
        restaurant = cursor.fetchone()
        conn.close()
        
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        return jsonify(dict_from_row(restaurant)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MENUS ====================

@app.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    """Get menu items for a restaurant"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu_items WHERE restaurant_id = %s", (restaurant_id,))
        menu_items = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(menu_items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get specific menu item"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            return jsonify({'error': 'Menu item not found'}), 404
        
        return jsonify(dict_from_row(item)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CUSTOMERS ====================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Check if customers table exists
        cursor.execute("SHOW TABLES LIKE 'customers'")
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Customers table does not exist. Please run the database migration.'}), 404
        
        cursor.execute("SELECT * FROM customers ORDER BY name ASC")
        customers = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(customers), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_customers: {error_details}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get specific customer"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        return jsonify(dict_from_row(customer)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        address = data.get('address', '')
        city = data.get('city', '')
        
        if not name or not email:
            return jsonify({'error': 'Name and email are required'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO customers (name, email, phone, address, city)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, address, city))
        
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': customer_id,
            'name': name,
            'email': email,
            'message': 'Customer created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/find-or-create', methods=['POST'])
def find_or_create_customer():
    """Find customer by email or create/update if not exists"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '')
        address = data.get('address', '')
        city = data.get('city', '')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Check if customers table exists
        cursor.execute("SHOW TABLES LIKE 'customers'")
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Customers table does not exist'}), 404
        
        customer_id = None
        
        # If email provided, try to find by email
        if email:
            cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
            existing = cursor.fetchone()
            if existing:
                customer_id = existing['id']
                # Update customer information
                cursor.execute("""
                    UPDATE customers 
                    SET name = %s, phone = %s, address = %s, city = %s
                    WHERE id = %s
                """, (name, phone, address, city, customer_id))
                conn.commit()
        else:
            # If no email, try to find by name (less reliable, but works)
            cursor.execute("SELECT * FROM customers WHERE name = %s LIMIT 1", (name,))
            existing = cursor.fetchone()
            if existing:
                customer_id = existing['id']
                # Update customer information
                cursor.execute("""
                    UPDATE customers 
                    SET phone = %s, address = %s, city = %s
                    WHERE id = %s
                """, (phone, address, city, customer_id))
                conn.commit()
        
        # If customer not found, create new one
        if not customer_id:
            # Generate email if not provided
            if not email:
                email = f"{name.lower().replace(' ', '.')}@fooddelivery.com"
                # Make sure email is unique
                counter = 1
                original_email = email
                while True:
                    cursor.execute("SELECT id FROM customers WHERE email = %s", (email,))
                    if not cursor.fetchone():
                        break
                    email = f"{original_email.split('@')[0]}{counter}@fooddelivery.com"
                    counter += 1
            
            cursor.execute("""
                INSERT INTO customers (name, email, phone, address, city)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, address, city))
            customer_id = cursor.lastrowid
            conn.commit()
        
        # Get the final customer data
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'id': customer_id,
            'customer': dict_from_row(customer),
            'message': 'Customer found/created successfully'
        }), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in find_or_create_customer: {error_details}")
        return jsonify({'error': str(e)}), 500

# ==================== DELIVERY STAFF ====================

@app.route('/api/delivery-staff', methods=['GET'])
def get_delivery_staff():
    """Get all delivery staff"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Check if delivery_staff table exists
        cursor.execute("SHOW TABLES LIKE 'delivery_staff'")
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Delivery staff table does not exist. Please run the database migration.'}), 404
        
        status_filter = request.args.get('status')
        
        if status_filter:
            cursor.execute("SELECT * FROM delivery_staff WHERE status = %s ORDER BY name ASC", (status_filter,))
        else:
            cursor.execute("SELECT * FROM delivery_staff ORDER BY name ASC")
        
        staff = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(staff), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_delivery_staff: {error_details}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delivery-staff/<int:staff_id>', methods=['GET'])
def get_delivery_staff_member(staff_id):
    """Get specific delivery staff member"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM delivery_staff WHERE id = %s", (staff_id,))
        staff = cursor.fetchone()
        conn.close()
        
        if not staff:
            return jsonify({'error': 'Delivery staff not found'}), 404
        
        return jsonify(dict_from_row(staff)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delivery-staff/available', methods=['GET'])
def get_available_delivery_staff():
    """Get available delivery staff"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Check if delivery_staff table exists
        cursor.execute("SHOW TABLES LIKE 'delivery_staff'")
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Delivery staff table does not exist. Please run the database migration.'}), 404
        
        cursor.execute("""
            SELECT * FROM delivery_staff 
            WHERE status = 'Available' 
            ORDER BY rating DESC, total_deliveries ASC
        """)
        staff = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(staff), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_available_delivery_staff: {error_details}")
        return jsonify({'error': str(e)}), 500

# ==================== ORDERS ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Check if new columns exist, use appropriate query
        try:
            # Try to get column names from orders table
            cursor.execute("SHOW COLUMNS FROM orders LIKE 'customer_id'")
            has_customer_id = cursor.fetchone() is not None
            
            if has_customer_id:
                # Use enhanced query with customer and delivery staff
                cursor.execute("""
                    SELECT o.id, o.customer_id, o.restaurant_id, o.delivery_staff_id, o.total_price, o.status, 
                           o.created_at, o.updated_at, 
                           COALESCE(o.delivery_address, '') as delivery_address,
                           COALESCE(o.payment_method, '') as payment_method,
                           GROUP_CONCAT(CONCAT(mi.name, ' x', oi.quantity) SEPARATOR ', ') as items,
                           r.name as restaurant_name,
                           COALESCE(c.name, 'Guest') as customer_name,
                           COALESCE(c.email, '') as customer_email,
                           COALESCE(ds.name, '') as delivery_staff_name
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                    LEFT JOIN restaurants r ON o.restaurant_id = r.id
                    LEFT JOIN customers c ON o.customer_id = c.id
                    LEFT JOIN delivery_staff ds ON o.delivery_staff_id = ds.id
                    GROUP BY o.id
                    ORDER BY o.created_at DESC
                """)
            else:
                # Use basic query for old schema
                cursor.execute("""
                    SELECT o.id, o.restaurant_id, o.total_price, o.status, o.created_at, o.updated_at,
                           GROUP_CONCAT(CONCAT(mi.name, ' x', oi.quantity) SEPARATOR ', ') as items,
                           r.name as restaurant_name
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                    LEFT JOIN restaurants r ON o.restaurant_id = r.id
                    GROUP BY o.id
                    ORDER BY o.created_at DESC
                """)
        except Exception as schema_error:
            # Fallback to simplest query if schema check fails
            cursor.execute("""
                SELECT o.id, o.restaurant_id, o.total_price, o.status, o.created_at, o.updated_at,
                       GROUP_CONCAT(CONCAT(mi.name, ' x', oi.quantity) SEPARATOR ', ') as items,
                       r.name as restaurant_name
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                LEFT JOIN restaurants r ON o.restaurant_id = r.id
                GROUP BY o.id
                ORDER BY o.created_at DESC
            """)
        
        orders = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(orders), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_orders: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        customer_id = data.get('customer_id', 1)  # Default to customer 1 if not provided
        restaurant_id = data.get('restaurant_id')
        items = data.get('items')  # List of {menu_item_id, quantity}
        delivery_address = data.get('delivery_address', '')
        payment_method = data.get('payment_method', 'Cash')
        
        if not restaurant_id or not items:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Verify customer exists (if customers table exists)
        try:
            cursor.execute("SHOW TABLES LIKE 'customers'")
            customers_table_exists = cursor.fetchone() is not None
            
            if customers_table_exists:
                cursor.execute("SELECT id FROM customers WHERE id = %s", (customer_id,))
                if not cursor.fetchone():
                    conn.close()
                    return jsonify({'error': f"Customer {customer_id} not found"}), 404
        except:
            # If customers table doesn't exist, use default customer_id = 1
            customer_id = 1
        
        # Calculate total price from items
        calculated_total = 0
        item_details = []
        
        for item in items:
            # Get item price from database
            cursor.execute("SELECT price FROM menu_items WHERE id = %s", (item['menu_item_id'],))
            menu_item = cursor.fetchone()
            
            if not menu_item:
                conn.close()
                return jsonify({'error': f"Menu item {item['menu_item_id']} not found"}), 404
            
            item_price = dict_from_row(menu_item)['price']
            item_quantity = item['quantity']
            calculated_total += item_price * item_quantity
            item_details.append({
                'menu_item_id': item['menu_item_id'],
                'quantity': item_quantity,
                'price': item_price
            })
        
        # Check if new columns exist
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'customer_id'")
        has_customer_id = cursor.fetchone() is not None
        
        # Auto-assign available delivery staff
        delivery_staff_id = None
        initial_status = 'Pending'
        if has_customer_id:
            try:
                cursor.execute("SHOW TABLES LIKE 'delivery_staff'")
                if cursor.fetchone():
                    # Find available delivery staff with highest rating
                    cursor.execute("""
                        SELECT id FROM delivery_staff 
                        WHERE status = 'Available' 
                        ORDER BY rating DESC, total_deliveries ASC 
                        LIMIT 1
                    """)
                    staff = cursor.fetchone()
                    if staff:
                        delivery_staff_id = staff['id']
                        # Update delivery staff status to Busy
                        cursor.execute("""
                            UPDATE delivery_staff 
                            SET status = 'Busy', total_deliveries = total_deliveries + 1
                            WHERE id = %s
                        """, (delivery_staff_id,))
                        # If we successfully assign a staff at creation, set the order status to Out for Delivery
                        initial_status = 'Out for Delivery'
            except Exception as e:
                print(f"Error assigning delivery staff: {e}")
                pass
        
        # Create order with calculated total (handle both old and new schema)
        if has_customer_id:
            cursor.execute("""
                INSERT INTO orders (customer_id, restaurant_id, delivery_staff_id, total_price, status, 
                                  delivery_address, payment_method, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer_id, restaurant_id, delivery_staff_id, calculated_total, initial_status,
                  delivery_address, payment_method, datetime.now()))
        else:
            # Old schema without customer_id
            cursor.execute("""
                INSERT INTO orders (restaurant_id, total_price, status, created_at)
                VALUES (%s, %s, 'Pending', %s)
            """, (restaurant_id, calculated_total, datetime.now()))
        
        order_id = cursor.lastrowid
        
        # Add order items with prices
        for item_detail in item_details:
            cursor.execute("""
                INSERT INTO order_items (order_id, menu_item_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item_detail['menu_item_id'], item_detail['quantity'], item_detail['price']))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': order_id,
            'customer_id': customer_id,
            'restaurant_id': restaurant_id,
            'delivery_staff_id': delivery_staff_id,
            'total_price': calculated_total,
            'status': 'Pending',
            'message': 'Order created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, 
                   r.name as restaurant_name,
                   c.name as customer_name,
                   c.email as customer_email,
                   c.phone as customer_phone,
                   c.address as customer_address,
                   ds.name as delivery_staff_name,
                   ds.phone as delivery_staff_phone,
                   ds.vehicle_type
            FROM orders o
            LEFT JOIN restaurants r ON o.restaurant_id = r.id
            LEFT JOIN customers c ON o.customer_id = c.id
            LEFT JOIN delivery_staff ds ON o.delivery_staff_id = ds.id
            WHERE o.id = %s
        """, (order_id,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return jsonify({'error': 'Order not found'}), 404
        
        cursor.execute("""
            SELECT oi.*, mi.name, mi.price
            FROM order_items oi
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        items = [dict_from_row(row) for row in cursor.fetchall()]
        order_dict = dict_from_row(order)
        order_dict['items'] = items
        conn.close()
        
        return jsonify(order_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        # Update order status
        cursor.execute("UPDATE orders SET status = %s, updated_at = %s WHERE id = %s", (status, datetime.now(), order_id))

        # If the status was changed to Out for Delivery, ensure a delivery staff is assigned
        if status == 'Out for Delivery':
            # Check if order already has a delivery_staff
            cursor.execute("SELECT delivery_staff_id FROM orders WHERE id = %s", (order_id,))
            row = cursor.fetchone()
            delivery_staff_id = row.get('delivery_staff_id') if row else None

            if not delivery_staff_id:
                try:
                    # Find best available delivery staff
                    cursor.execute("SHOW TABLES LIKE 'delivery_staff'")
                    if cursor.fetchone():
                        cursor.execute("""
                            SELECT id FROM delivery_staff 
                            WHERE status = 'Available' 
                            ORDER BY rating DESC, total_deliveries ASC 
                            LIMIT 1
                        """)
                        staff = cursor.fetchone()
                        if staff:
                            ds_id = staff['id']
                            cursor.execute("UPDATE orders SET delivery_staff_id = %s WHERE id = %s", (ds_id, order_id))
                            cursor.execute("UPDATE delivery_staff SET status = 'Busy', total_deliveries = total_deliveries + 1 WHERE id = %s", (ds_id,))
                except Exception as e:
                    print(f"Error assigning delivery staff on status update: {e}")

        # If status changed to Delivered, mark assigned delivery staff as Available
        if status == 'Delivered':
            try:
                cursor.execute("SELECT delivery_staff_id FROM orders WHERE id = %s", (order_id,))
                od = cursor.fetchone()
                if od and od.get('delivery_staff_id'):
                    cursor.execute("UPDATE delivery_staff SET status = 'Available' WHERE id = %s", (od['delivery_staff_id'],))
            except Exception as e:
                print(f"Error releasing delivery staff on delivered: {e}")

        conn.commit()
        conn.close()

        return jsonify({'message': 'Order updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Delete order items first
        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
        # Delete order
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>/items', methods=['POST'])
def add_order_item(order_id):
    """Add an item to an existing order"""
    try:
        data = request.get_json()
        menu_item_id = data.get('menu_item_id')
        quantity = data.get('quantity', 1)
        
        if not menu_item_id:
            return jsonify({'error': 'Menu item ID is required'}), 400
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get menu item price
        cursor.execute("SELECT price FROM menu_items WHERE id = %s", (menu_item_id,))
        menu_item = cursor.fetchone()
        
        if not menu_item:
            conn.close()
            return jsonify({'error': 'Menu item not found'}), 404
        
        item_price = dict_from_row(menu_item)['price']
        
        # Check if item already exists in this order
        cursor.execute("""
            SELECT id, quantity FROM order_items 
            WHERE order_id = %s AND menu_item_id = %s
        """, (order_id, menu_item_id))
        
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity if item exists
            existing_dict = dict_from_row(existing_item)
            new_quantity = existing_dict['quantity'] + quantity
            cursor.execute("""
                UPDATE order_items 
                SET quantity = %s 
                WHERE id = %s
            """, (new_quantity, existing_dict['id']))
        else:
            # Add new item
            cursor.execute("""
                INSERT INTO order_items (order_id, menu_item_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, menu_item_id, quantity, item_price))
        
        # Update order total price
        cursor.execute("""
            SELECT SUM(oi.quantity * oi.price) as total
            FROM order_items oi
            WHERE oi.order_id = %s
        """, (order_id,))
        
        total_result = cursor.fetchone()
        total_value = dict_from_row(total_result).get('total') if total_result else 0
        new_total = total_value or 0
        
        cursor.execute("""
            UPDATE orders SET total_price = %s WHERE id = %s
        """, (new_total, order_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Item added successfully',
            'new_total': new_total
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>/items/<int:item_id>', methods=['DELETE'])
def remove_order_item(order_id, item_id):
    """Remove an item from an order"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Delete the order item
        cursor.execute("""
            DELETE FROM order_items 
            WHERE order_id = %s AND id = %s
        """, (order_id, item_id))
        
        # Update order total price
        cursor.execute("""
            SELECT SUM(oi.quantity * oi.price) as total
            FROM order_items oi
            WHERE oi.order_id = %s
        """, (order_id,))
        
        total_result = cursor.fetchone()
        total_value = dict_from_row(total_result).get('total') if total_result else 0
        new_total = total_value or 0
        
        cursor.execute("""
            UPDATE orders SET total_price = %s WHERE id = %s
        """, (new_total, order_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Item removed successfully',
            'new_total': new_total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== AUTOMATIC STATUS UPDATE ====================

def update_order_statuses():
    """Background task to automatically update order statuses every 10 seconds"""
    # Status progression order
    status_sequence = ['Pending', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered']
    
    while True:
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            
            # Get all orders that are not Delivered or Cancelled
            cursor.execute("""
                SELECT id, status, created_at, updated_at, delivery_staff_id
                FROM orders 
                WHERE status NOT IN ('Delivered', 'Cancelled')
                ORDER BY created_at ASC
            """)
            
            orders = cursor.fetchall()
            current_time = datetime.now()
            
            for order in orders:
                order_id = order['id']
                current_status = order['status']
                
                # Parse created_at timestamp (handle different formats)
                created_at = order['created_at']
                if isinstance(created_at, datetime):
                    # Already a datetime object
                    pass
                elif isinstance(created_at, str):
                    # Parse string format
                    try:
                        # Remove microseconds if present
                        created_at_str = created_at.split('.')[0] if '.' in created_at else created_at
                        created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        print(f"Warning: Could not parse created_at for order {order_id}: {created_at}")
                        continue
                else:
                    # Try to convert other datetime-like objects
                    try:
                        if hasattr(created_at, 'timestamp'):
                            created_at = datetime.fromtimestamp(created_at.timestamp())
                        else:
                            print(f"Warning: Unexpected created_at type for order {order_id}: {type(created_at)}")
                            continue
                    except Exception as e:
                        print(f"Warning: Could not convert created_at for order {order_id}: {e}")
                        continue
                
                # Calculate seconds since order creation
                seconds_elapsed = (current_time - created_at).total_seconds()
                
                # Determine target status based on 10-second intervals
                # 0-10 sec: Pending, 10-20 sec: Confirmed, 20-30 sec: Preparing, 30-40 sec: Out for Delivery, 40+ sec: Delivered
                interval_index = min(int(seconds_elapsed / 10), len(status_sequence) - 1)
                target_status = status_sequence[interval_index]
                
                # Only update if status needs to change
                if current_status != target_status:
                    cursor.execute("""
                        UPDATE orders 
                        SET status = %s, updated_at = %s 
                        WHERE id = %s
                    """, (target_status, current_time, order_id))
                    
                    # If order is delivered, set delivery staff back to Available
                    if target_status == 'Delivered':
                        cursor.execute("""
                            SELECT delivery_staff_id FROM orders WHERE id = %s
                        """, (order_id,))
                        order_data = cursor.fetchone()
                        if order_data and order_data.get('delivery_staff_id'):
                            cursor.execute("""
                                UPDATE delivery_staff 
                                SET status = 'Available' 
                                WHERE id = %s
                            """, (order_data['delivery_staff_id'],))
                    
                    print(f"Order #{order_id} status updated: {current_status} -> {target_status}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating order statuses: {e}")
            try:
                conn.close()
            except:
                pass
        
        # Wait 10 seconds before next check
        time.sleep(10)

def start_status_update_thread():
    """Start the background thread for automatic status updates"""
    status_thread = threading.Thread(target=update_order_statuses, daemon=True)
    status_thread.start()
    print("✅ Automatic order status update thread started")

# ==================== REPORTS & ANALYTICS ====================

@app.route('/api/reports/summary', methods=['GET'])
def get_summary_report():
    """Get summary statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get counts (check if tables exist first)
        total_customers = 0
        total_delivery_staff = 0
        
        cursor.execute("SHOW TABLES LIKE 'customers'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) as count FROM customers")
            total_customers = cursor.fetchone()['count']
        
        cursor.execute("SHOW TABLES LIKE 'delivery_staff'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) as count FROM delivery_staff")
            total_delivery_staff = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM restaurants")
        total_restaurants = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        total_orders = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(total_price) as total FROM orders")
        total_revenue = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT AVG(total_price) as avg FROM orders")
        avg_order_value = cursor.fetchone()['avg'] or 0
        
        conn.close()
        
        return jsonify({
            'total_customers': total_customers,
            'total_restaurants': total_restaurants,
            'total_delivery_staff': total_delivery_staff,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'avg_order_value': float(avg_order_value)
        }), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_summary_report: {error_details}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/orders-by-status', methods=['GET'])
def get_orders_by_status():
    """Get order count grouped by status"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM orders 
            GROUP BY status
            ORDER BY count DESC
        """)
        results = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/restaurant-revenue', methods=['GET'])
def get_restaurant_revenue():
    """Get revenue by restaurant"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                r.id,
                r.name as restaurant_name,
                r.cuisine,
                COUNT(o.id) as order_count,
                SUM(o.total_price) as total_revenue,
                AVG(o.total_price) as avg_order_value
            FROM restaurants r
            LEFT JOIN orders o ON r.id = o.restaurant_id
            GROUP BY r.id, r.name, r.cuisine
            ORDER BY total_revenue DESC
        """)
        results = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/top-customers', methods=['GET'])
def get_top_customers():
    """Get top customers by spending"""
    try:
        limit = request.args.get('limit', 5, type=int)
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                c.email,
                COUNT(o.id) as order_count,
                SUM(o.total_price) as total_spent,
                AVG(o.total_price) as avg_order_value
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.email
            HAVING total_spent > 0
            ORDER BY total_spent DESC
            LIMIT %s
        """, (limit,))
        results = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Backend is running'}), 200

if __name__ == '__main__':
    # Start background thread for automatic status updates
    start_status_update_thread()
    app.run(debug=True, port=5000)
