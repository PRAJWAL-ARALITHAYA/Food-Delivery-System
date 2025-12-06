import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodHub Database Viewer")
        self.root.geometry("1000x600")
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(self.main_frame, text="🍕 FoodHub Database Viewer", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Buttons
        ttk.Button(self.main_frame, text="View All Orders", command=self.view_orders).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.main_frame, text="View Menu Items", command=self.view_menu).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.main_frame, text="View Restaurants", command=self.view_restaurants).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Export Orders (CSV)", command=self.export_csv).grid(row=1, column=3, padx=5, pady=5)
        
        # Tree view
        self.tree = ttk.Treeview(self.main_frame)
        self.tree.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=2, column=4, sticky=(tk.N, tk.S))
        self.tree.configure(yscroll=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
    
    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def view_orders(self):
        self.clear_tree()
        self.tree['columns'] = ('ID', 'Restaurant', 'Total', 'Status', 'Created')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=40)
        self.tree.column('Restaurant', anchor=tk.W, width=200)
        self.tree.column('Total', anchor=tk.W, width=100)
        self.tree.column('Status', anchor=tk.W, width=120)
        self.tree.column('Created', anchor=tk.W, width=200)
        
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('Restaurant', text='Restaurant', anchor=tk.W)
        self.tree.heading('Total', text='Total Price', anchor=tk.W)
        self.tree.heading('Status', text='Status', anchor=tk.W)
        self.tree.heading('Created', text='Created', anchor=tk.W)
        
        try:
            conn = sqlite3.connect('backend/food_delivery.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.id, r.name as restaurant, o.total_price, o.status, o.created_at
                FROM orders o
                LEFT JOIN restaurants r ON o.restaurant_id = r.id
                ORDER BY o.id DESC
            """)
            
            for row in cursor.fetchall():
                r = dict(row)
                self.tree.insert('', 'end', values=(
                    r['id'],
                    r['restaurant'],
                    f"Rs {r['total_price']}",
                    r['status'],
                    r['created_at']
                ))
            
            conn.close()
            self.status_var.set(f"Loaded {len(self.tree.get_children())} orders")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")
    
    def view_menu(self):
        self.clear_tree()
        self.tree['columns'] = ('ID', 'Item', 'Restaurant', 'Category', 'Price')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=40)
        self.tree.column('Item', anchor=tk.W, width=250)
        self.tree.column('Restaurant', anchor=tk.W, width=150)
        self.tree.column('Category', anchor=tk.W, width=120)
        self.tree.column('Price', anchor=tk.W, width=100)
        
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('Item', text='Item Name', anchor=tk.W)
        self.tree.heading('Restaurant', text='Restaurant', anchor=tk.W)
        self.tree.heading('Category', text='Category', anchor=tk.W)
        self.tree.heading('Price', text='Price', anchor=tk.W)
        
        try:
            conn = sqlite3.connect('backend/food_delivery.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT m.id, m.name, r.name as restaurant, m.category, m.price
                FROM menu_items m
                LEFT JOIN restaurants r ON m.restaurant_id = r.id
                ORDER BY r.name, m.name
            """)
            
            for row in cursor.fetchall():
                m = dict(row)
                self.tree.insert('', 'end', values=(
                    m['id'],
                    m['name'],
                    m['restaurant'],
                    m['category'],
                    f"Rs {m['price']}"
                ))
            
            conn.close()
            self.status_var.set(f"Loaded {len(self.tree.get_children())} menu items")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")
    
    def view_restaurants(self):
        self.clear_tree()
        self.tree['columns'] = ('ID', 'Name', 'Cuisine', 'Rating', 'Delivery')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=40)
        self.tree.column('Name', anchor=tk.W, width=200)
        self.tree.column('Cuisine', anchor=tk.W, width=150)
        self.tree.column('Rating', anchor=tk.W, width=100)
        self.tree.column('Delivery', anchor=tk.W, width=100)
        
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('Name', text='Name', anchor=tk.W)
        self.tree.heading('Cuisine', text='Cuisine', anchor=tk.W)
        self.tree.heading('Rating', text='Rating', anchor=tk.W)
        self.tree.heading('Delivery', text='Delivery (min)', anchor=tk.W)
        
        try:
            conn = sqlite3.connect('backend/food_delivery.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name, cuisine, rating, delivery_time FROM restaurants ORDER BY id")
            
            for row in cursor.fetchall():
                r = dict(row)
                self.tree.insert('', 'end', values=(
                    r['id'],
                    r['name'],
                    r['cuisine'],
                    r['rating'],
                    r['delivery_time']
                ))
            
            conn.close()
            self.status_var.set(f"Loaded {len(self.tree.get_children())} restaurants")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")
    
    def export_csv(self):
        try:
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
            
            import csv
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Order ID', 'Restaurant', 'Total Price', 'Status', 'Created'])
                for row in cursor.fetchall():
                    r = dict(row)
                    writer.writerow([r['id'], r['restaurant'], r['total_price'], r['status'], r['created_at']])
            
            conn.close()
            messagebox.showinfo("Success", f"Orders exported to {filename}")
            self.status_var.set(f"Exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set(f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    app.view_orders()  # Load orders by default
    root.mainloop()
